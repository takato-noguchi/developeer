import json
#from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
#from asgiref.sync import async_to_sync  # async_to_sync() : 非同期関数を同期的に実行する際に使用する。
import datetime

# ChatConsumerクラス: WebSocketからの受け取ったものを処理するクラス
class ChatConsumer( AsyncWebsocketConsumer ):

    # コンストラクタ
    def __init__( self, *args, **kwargs ):
        super().__init__( *args, **kwargs )
        self.strGroupName = ''
        self.strUserName = ''

    # WebSocket接続時の処理
    async def connect( self ):
        # WebSocket接続を受け入れます。
        # ・connect()でaccept()を呼び出さないと、接続は拒否されて閉じられます。
        # 　たとえば、要求しているユーザーが要求されたアクションを実行する権限を持っていないために、接続を拒否したい場合があります。
        # 　接続を受け入れる場合は、connect()の最後のアクションとしてaccept()を呼び出します。
        await self.accept()

    # WebSocket切断時の処理
    async def disconnect( self, close_code ):
        # チャットからの離脱
        await self.leave_chat()

    # WebSocketからのデータ受信時の処理
    # （ブラウザ側のJavaScript関数のsocketChat.send()の結果、WebSocketを介してデータがChatConsumerに送信され、本関数で受信処理します）
    async def receive( self, text_data ):
        # 受信データをJSONデータに復元
        text_data_json = json.loads( text_data )

        # チャットへの参加時の処理
        if( 'join' == text_data_json.get( 'data_type' ) ):
            # ユーザー名をクラスメンバー変数に設定
            self.strUserName = text_data_json['username']
            # ルーム名の取得
            strRoomName = text_data_json['roomname']
            # チャットへの参加
            await self.join_chat( strRoomName )

    # 拡散メッセージ受信時の処理
    # （self.channel_layer.group_send()の結果、グループ内の全コンシューマーにメッセージ拡散され、各コンシューマーは本関数で受信処理します）
    async def chat_message( self, data ):
        data_json = {
            'message': data['message'],
            'username': data['username'],
            'datetime': data['datetime'],
        }

        # WebSocketにメッセージを送信します。
        # （送信されたメッセージは、ブラウザ側のJavaScript関数のsocketChat.onmessage()で受信処理されます）
        # JSONデータをテキストデータにエンコードして送ります。
        await self.send( text_data=json.dumps( data_json ) )

    # チャットへの参加
    async def join_chat( self, strRoomName ):
        # グループに参加
        #self.strGroupName = 'chat'
        self.strGroupName = 'chat_%s' % strRoomName
        await self.channel_layer.group_add( self.strGroupName, self.channel_name )

    # チャットからの離脱
    async def leave_chat( self ):
        if( '' == self.strGroupName ):
            return

        # グループから離脱
        await self.channel_layer.group_discard( self.strGroupName, self.channel_name )

        # ルーム名を空に
        self.strGroupName = ''