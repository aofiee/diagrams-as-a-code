from diagrams import Cluster, Diagram, Edge
from diagrams.onprem.client import Client, Users, User
from diagrams.gcp.network import DNS, LoadBalancing
from diagrams.gcp.compute import KubernetesEngine
from diagrams.onprem.network import Nginx, Kong
from diagrams.onprem.database import MongoDB, MySQL
from diagrams.programming.framework import React, Flutter
from diagrams.programming.language import NodeJS
from diagrams.firebase.develop import Authentication, Hosting, Functions, Firestore, Storage
from diagrams.gcp.database import SQL
from diagrams.gcp.analytics import Pubsub
from diagrams.firebase.grow import Messaging, RemoteConfig
from diagrams.firebase.quality import AppDistribution, Crashlytics, PerformanceMonitoring
graph_attr = {
    "fontsize": "18",
}
graph_attr2 = {
    "pad": "10.0",
    "fontsize": "18",
}


def draw():
    with Diagram("Example Microservice for EBA", show=False, graph_attr=graph_attr, direction="LR"):
        staff = Client('EBA Staff')
        organinzer = User("EBA Organinzer")
        users = Users("EBA Users")
        mobileApp = Flutter("EBA Mobile")
        dns = DNS('Cloud DNS')
        loadbalance = LoadBalancing('Cloud Loadbalancing')
        auth = Authentication("Firebase Auth")
        users >> Edge(color="darkgreen") >> mobileApp << Edge(
            color="darkgreen") >> auth
        [organinzer, staff] << Edge(color="darkgreen") >> dns
        dns << Edge(color="darkgreen") >> loadbalance

        with Cluster("Google Cloud Platform", graph_attr=graph_attr2):
            with Cluster("WEB Frontend", graph_attr=graph_attr2):
                with Cluster("Web Container1", graph_attr=graph_attr2):
                    web1 = Hosting("Firebase Hosting")
                    react1 = React("Frontend")
                    web1 - react1
                with Cluster("Web Container2", graph_attr=graph_attr2):
                    web2 = Hosting("Firebase Hosting")
                    react2 = React("Frontend")
                    web2 - react2
            with Cluster("WEB Backend", graph_attr=graph_attr2):
                with Cluster("Web Backend Container"):
                    web3 = Hosting("Firebase Hosting")
                    react3 = React("Backend")
                    web3 - react3
            loadbalance << Edge(color="darkgreen") >> [web1, web2, web3]
            with Cluster("APIs", graph_attr=graph_attr2):
                func = Functions("Cloud Functions")
                remoteCnf = RemoteConfig("RemoteConfig")
                [react1, react2, react3] << Edge(
                    color="darkgreen") >> remoteCnf << Edge(
                    color="darkgreen") >> func
                with Cluster("Feeds", graph_attr=graph_attr2):
                    apiFeeds = NodeJS("Express")
                with Cluster("Tournaments", graph_attr=graph_attr2):
                    apiTournament = NodeJS("Express")
                with Cluster("Badges", graph_attr=graph_attr2):
                    apiBadges = NodeJS("Express")
                with Cluster("User", graph_attr=graph_attr2):
                    apiUser = NodeJS("Express")
                with Cluster("Games", graph_attr=graph_attr2):
                    apiGames = NodeJS("Express")
                with Cluster("Notifications", graph_attr=graph_attr2):
                    apiNotifications = NodeJS("Express")
                auth << Edge(color="darkgreen") >> func >> Edge(color="darkorange") >> [apiBadges, apiUser, apiFeeds,
                                                                                        apiGames, apiNotifications, apiTournament]
            with Cluster("Database", graph_attr=graph_attr2):
                badgesSQL = SQL("Badges")
                userSQL = SQL("User")
                notificationSQL = SQL("Notifications")
                tournamentsSQL = SQL("Tournaments")
                gamesSQL = SQL("Games")
                feedsSQL = SQL("Feeds")

                apiBadges - Edge(color="darkorange") - badgesSQL
                apiUser - Edge(color="darkorange") - userSQL
                apiFeeds - Edge(color="darkorange") - feedsSQL
                apiGames - Edge(color="darkorange") - gamesSQL
                apiNotifications - Edge(color="darkorange") - notificationSQL
                apiTournament - Edge(color="darkorange") - tournamentsSQL

                firestore = Firestore("Firestore")

            with Cluster("Message Queue", graph_attr=graph_attr2):
                messageQueue = Pubsub("Pubsub")
            [badgesSQL, userSQL, notificationSQL, tournamentsSQL,
                gamesSQL, feedsSQL] >> Edge(color="darkorange") >> messageQueue

            messageQueue >> Edge(color="darkred") >> firestore >> Edge(color="darkred", style="dotted") >> [apiBadges, apiUser, apiFeeds,
                                                                                                            apiGames, apiNotifications, apiTournament]
            with Cluster("Storage", graph_attr=graph_attr2):
                badgesStorage = Storage("Badges")
                userStorage = Storage("User")
                gameStorage = Storage("Games")
                tournamentsStorage = Storage("Tournaments")
            apiBadges - Edge(color="blue") - badgesStorage
            apiUser - Edge(color="blue") - userStorage
            apiGames - Edge(color="blue") - gameStorage
            apiTournament - Edge(color="blue") - tournamentsStorage

            fcm = Messaging("Cloud Messaging")
            apiNotifications >> \
                Edge(color="darkorange") >> \
                fcm >> Edge(color="darkgreen") >> auth


if __name__ == '__main__':
    draw()
