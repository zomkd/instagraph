"""Api urls"""
from django.urls import path
from .api import (
                InstUser, UserLikers, UserInfo,
                UserReverseActivity, UserLikersGraph, 
                UserCommonFollowingsGraph, UserUnionGraph,
                UserFollowings, UserCSVWriter, PostLocation,
                UserDelete,
                )


app_name = "backend"

urlpatterns = [
    path('username/', InstUser.as_view()),
    path('user_info/', UserInfo.as_view()),
    path('user_delete/',UserDelete.as_view()),
    path('user_likers/', UserLikers.as_view()),
    path('user_likers_graph/', UserLikersGraph.as_view()),
    path('user_common_followings_graph/', UserCommonFollowingsGraph.as_view()),
    path('user_union_graph/', UserUnionGraph.as_view()),
    path('user_reverse_activity/', UserReverseActivity.as_view()),
    path('user_followings/', UserFollowings.as_view()),
    path('user_csv_writer/', UserCSVWriter.as_view()),
    path('post_location/', PostLocation.as_view()),
]
