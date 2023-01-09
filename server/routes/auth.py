from datetime import datetime, timedelta
from bson.objectid import ObjectId
from fastapi import APIRouter, Response, status, Depends, HTTPException, Body

from server import oauth2
from server.oauth2 import AuthJWT
from server.config.config import settings
from server.connect import user_collection
from server import utils
from server.models.user import UserBaseSchema, CreateUserSchema, LoginUserSchema, UserResponseSchema
from server.config.response import ResponseModel, ErrorResponseModel
from server.databases.auth import userResponseEntity, embeddedUserResponse, userEntity

router = APIRouter()
ACCESS_TOKEN_EXPIRES_IN = settings.ACCESS_TOKEN_EXPIRES_IN
REFRESH_TOKEN_EXPIRES_IN = settings.REFRESH_TOKEN_EXPIRES_IN


@router.post('/register')
async def create_user(payload: CreateUserSchema):
    # Check if user already exist
    user = await user_collection.find_one({'email': payload.email.lower()})
    if user:
        return ErrorResponseModel(
            "User already exist", status.HTTP_400_BAD_REQUEST, "User already exist")
    # Compare password and passwordConfirm
    if payload.password != payload.passwordConfirm:
        return ErrorResponseModel(
            "Password and Password Confirm don't match", 400, "Password and Password Confirm don't match")
    #  Hash the password
    payload.password = utils.hash_password(payload.password)
    del payload.passwordConfirm
    payload.role = 'user'
    payload.verified = True
    payload.email = payload.email.lower()
    payload.created_at = datetime.utcnow()
    payload.updated_at = payload.created_at
    result = await user_collection.insert_one(payload.dict())
    new_user = userResponseEntity(await
                                  user_collection.find_one({'_id': result.inserted_id}))
    return ResponseModel(new_user, 'User created successfully')

@router.post('/login')
async def login(payload: LoginUserSchema, response: Response, Authorize: AuthJWT = Depends()):
    # Check if the user exist
    user = await user_collection.find_one({'email': payload.email.lower()})
    if not user:
        # raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
        #                     detail='Incorrect Email or Password')
        return ErrorResponseModel('Incorrect Email or Password', 400, 'Incorrect Email or Password')

    # Check if user verified his email
    if not user['verified']:
        return ErrorResponseModel('Please verify your email', 400, 'Please verify your email')
        # raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
        #                     detail='Please verify your email address')

    # Check if the password is valid
    if not utils.verify_password(payload.password, user['password']):
        return ErrorResponseModel('Incorrect Password', 400, 'Incorrect Password')
        # raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
        #                     detail='Incorrect Email or Password')

    # Create access token
    access_token = Authorize.create_access_token(
        subject=str(user["_id"]), expires_time=timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN))

    # Create refresh token
    refresh_token = Authorize.create_refresh_token(
        subject=str(user["_id"]), expires_time=timedelta(minutes=REFRESH_TOKEN_EXPIRES_IN))
    Authorize.set_access_cookies(access_token)
    Authorize.set_refresh_cookies(refresh_token)
    # Store refresh and access tokens in cookie
    response.set_cookie('access_token', access_token, ACCESS_TOKEN_EXPIRES_IN * 60,
                        ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')
    response.set_cookie('refresh_token', refresh_token,
                        REFRESH_TOKEN_EXPIRES_IN * 60, REFRESH_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')
    response.set_cookie('logged_in', 'True', ACCESS_TOKEN_EXPIRES_IN * 60,
                        ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, False, 'lax')

    # Send both access
    return ResponseModel({
        'access_token': access_token,
        'user': embeddedUserResponse(user)
    }, 'Logged in successfully')


@router.get('/refresh')
async def refresh_token(response: Response, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_refresh_token_required()

        user_id = Authorize.get_jwt_subject()
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not refresh access token')
        user = user_collection.find_one({'_id': ObjectId(str(user_id))})
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='The user belonging to this token no logger exist')
        access_token = Authorize.create_access_token(
            subject=str(user["id"]), expires_time=timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN))
    except Exception as e:
        error = e.__class__.__name__
        if error == 'MissingTokenError':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='Please provide refresh token')
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    response.set_cookie('access_token', access_token, ACCESS_TOKEN_EXPIRES_IN * 60,
                        ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')
    response.set_cookie('logged_in', 'True', ACCESS_TOKEN_EXPIRES_IN * 60,
                        ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, False, 'lax')
    return {'access_token': access_token}


@router.get('/logout', status_code=status.HTTP_200_OK)
async def logout(response: Response, Authorize: AuthJWT = Depends(), user_id: str = Depends(oauth2.require_user)):
    Authorize.unset_jwt_cookies()
    response.set_cookie('logged_in', '', -1)

    return {'status': 'success'}


@router.get('/me')
async def get_me(user_id: str = Depends(oauth2.require_user)):
    user = userResponseEntity(await user_collection.find_one(
        {'_id': ObjectId(str(user_id))}))
    return ResponseModel(user, 'User retrieved successfully')

#update user
@router.post('/update')
async def update_user(payload: UserResponseSchema, user_id: str = Depends(oauth2.require_user)):
    user = await user_collection.find_one({'_id': ObjectId(str(user_id))})
    if not user:
        return ErrorResponseModel('User not found', 404, 'User not found')
    update_result = await user_collection.update_one({'_id': ObjectId(str(user_id))}, {
        '$set': payload.dict(exclude_unset=True)})
    if update_result.modified_count == 1:
        return ResponseModel('User updated successfully', 'User updated successfully')
    return ErrorResponseModel('An error occurred', 500, 'An error occurred')

#get list user 
@router.get('/list')
async def get_list_user():
    users = []
    async for user in user_collection.find({"role": "user"}):
        users.append(userResponseEntity(user))
    return ResponseModel(users, 'List user')

