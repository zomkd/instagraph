import Vue from "vue"
import Router from "vue-router"
import UsernameForm from "../components/UsernameForm"
import UserInfo from "../components/UserInfo"
import UserLikersTable from "../components/UserLikersTable"
import UserGraph from "../components/UserGraph"
import UserCommonFollowingsGraph from "../components/UserCommonFollowingsGraph"
import UserUnionGraph from "../components/UserUnionGraph"
import UserReverseActivity from "../components/UserReverseActivity"

Vue.use(Router)

const routes = [
    {
        path: "/",
        name: "UsernameForm",
        component: UsernameForm,
    },
    {
        path: "/user_info",
        name: "UserInfo",
        component: UserInfo,
    },
    {
        path: "/user_likers/:username",
        name: "UserLikersTable",
        component: UserLikersTable,
    },
    {
        path: "/user_graph/:username",
        name: "UserGraph",
        component: UserGraph,
    },
    {
        path: "/user_common_followings_graph",
        name: "UserCommonFollowingsGraph",
        component: UserCommonFollowingsGraph,
    },
    {
        path: "/user_union_graph",
        name: "UserUnionGraph",
        component: UserUnionGraph,
    },
    {
        path: "/user_reverse_activity",
        name: "UserReverseActivity",
        component: UserReverseActivity,
    }
];


const router = new Router({
    mode: 'history',
    routes,
});

export default router;