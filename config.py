####################
## IRC Bot Config ##
####################

server1 = {
            # server to connect
            'host' : 'irc.freenode.net',

            # server port
            'port' : 6667,

            # channels to connect to (space as delimiter)
            'channels' : '##ihpbot-test-channel',

            # bot nick
            'nick' : 'ihpbot',

            # identify with NickServ? ( True or False )
            'nickserv' : False,

            # nickserv password
            'nickserv_pw' : '',

            # commands start with:
            'prefix' : '%',
}

admin = 'ihptru'

servers = ['server1']
