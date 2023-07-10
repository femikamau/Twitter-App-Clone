# Twitter Clone (API Documentation)

## Table of Contents

- [Introduction](#introduction)
- [Authentication](#authentication)
  - [Registration](#registration)
  - [Login](#login)
- [Accounts](#accounts)
- [Profiles](#profiles)
- [Posts](#posts)
  - [Feed](#feed)
  - [User Posts](#user-posts)
- [Comments](#comments)
- [Friends](#friends)

## Introduction

- Welcome to the Twitter Clone API Documentation. This documentation will help you understand the API endpoints and how to use them.

## Authentication

- All API endpoints require authentication. You can authenticate by sending your API key in the `Authorization` header.

### Registration

- To register an account, send a `POST` request to `/api/v1/register` with the following parameters:

  - `email`: The email of the account you want to register.
  - `first_name`: The first name of the account you want to register.
  - `last_name`: The last name of the account you want to register.
  - `username`: The username of the account you want to register.
  - `password`: The password of the account you want to register.

### Login

- To login to an account, send a `POST` request to `/api/v1/login` with the following parameters:

  - `username`: The username of the account you want to login to.
  - `password`: The password of the account you want to login to.

- Once you login, you will receive an API key. You can use this API key to authenticate your subsequent requests.

### Logout

- To logout of an account, send a `GET` request to `/api/v1/logout`. You must be authenticated to logout. This will invalidate your API key.

## Accounts

- Accounts are the users of the Twitter Clone API. Once you register an account, it automatically creates a profile for you.

## Profiles

- Profiles are the user profiles of the Twitter Clone API. You can view a user's profile by sending a `GET` request to `/api/v1/profiles/{username}`. This will return the following user information:

  - `url`: The URL of the user's profile.
  - `username`: The username of the user.
  - `avatar`: The avatar of the user.
  - `bio`: The bio of the user.
  - `followers`: The number of followers the user has.
  - `following`: The number of users the user is following.
  - `posts`: The number of posts the user has.

## Posts

- Posts are the tweets of the Twitter Clone API. You can either view posts from your feed or view posts from a user's profile. This will return the following post information:

  - `url`: The URL of the post.
  - `user`: The url of the profile of the user who created the post.
  - `content`: The content of the post.
  - `image`: The image of the post.
  - `created_at`: The date and time the post was created.
  - `updated_at`: The date and time the post was last updated.
  - `comments`: The number of comments the post has.

### Feed

- To view your feed, send a `GET` request to `/api/v1/posts/feed`. You must be authenticated to view your feed. This will return a list of both your posts and the posts of the users you follow. This endpoint is strictly read-only.

### User Posts

- To view a user's posts, send a `GET` request to `api/v1/profiles/{username}/posts`. This will return a list of the user's posts.

- If you are on your profile, `username = current_user_username`. Therefore
you can also view your posts by sending a `GET` request to `/api/v1/profiles/{username}/posts`.

## Comments

- Comments are the comments of the Twitter Clone API. You can either view comments from a post or create a comment on a post.

- To view a post's comments, send a `GET` request to `/api/v1/posts/{post_id}/comments`. This will return a list of the post's comments.

- To create a comment on a post, send a `POST` request to `/api/v1/posts/{post_id}/comments` with the following parameters:

  - `content`: The content of the comment you want to create.

- To retrieve a comment, send a `GET` request to `/api/v1/comments/{comment_id}`. This will return the following comment information:

  - `url`: The URL of the comment.
  - `content`: The content of the comment.
  - `author`: The author of the comment.
  - `post`: The post the comment belongs to.
  - `created_at`: The date and time the comment was created.
  - `updated_at`: The date and time the comment was last updated.

- To update a comment, the comment must belong to you. You send a `PUT` request to `/api/v1/comments/{comment_id}` with the following parameters:

  - `content`: The content of the comment you want to update.

- To delete a comment, the comment must belong to you. You send a `DELETE` request to `/api/v1/comments/{comment_id}`.

## Friends

- A user can follow another user and unfollow another user. In order to follow a user, you must send a `GET` request to `/api/v1/profiles/{username}/follow`. In order to unfollow a user, you must send a `GET` request to `/api/v1/profiles/{username}/unfollow`. You must be authenticated to follow or unfollow a user.

- To view a user's followers, send a `GET` request to `/api/v1/profiles/{username}/followers`. This will return a list of the user's followers.

- To view a user's following, send a `GET` request to `/api/v1/profiles/{username}/following`. This will return a list of the users the user is following.
