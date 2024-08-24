# GitHub Copilotの可能性を探る習作
## これは何？
　これはGitHub Copilotの支援を活用してほとんどのコードを生成して作ったアプリケーションです。
　このセクションから下のREADMEもCopilotに生成して貰いました。
　それ故に一部誤りがあったりユーザに有用性が無い情報だったりするけど、一応の意味があります。
　このプログラムを作るために必要だったCopilotへの指示はやり直しの合計で30にも満たず、そして人間が修正したのは10行にも満たないです。　取りあえず形を作るだけなら大体Copilot任せで十分で、一部の前後関係とか依存関係を修正してあげれば動く状態になりました。
　しかし、Copilotへの指示は適切な用語を用いて理解出来るエンジニア的な指示で無いと想定外の動きをするので、まだ素人がいくつかの機能を持つプログラムを作るのは難しいと感じます。
　他方で、知らないけどふんわり用語が解る所から手がかりを作る検索の代替としての有用性も示してくれました。　例えば、このプログラムを書き始める段階でWoLがあるとか、WoLはMACアドレスやマジックパケットと言うのが関連すると言う程度の知識しか無く、その詳しい内容は知りませんでした。　しかし、Copilotに「マジックパケットを送ってWakeUpする」と言う指示でパケット組み立ての部分が生成されたので情報を探して書く手間が省け、「マシン名からMACアドレスを取得する」と言う指示でgetmacと言うPyPiを利用するコードが生成されたのでPyPiを探す手間も省けました。
　そして、このアプリケーション自体も自宅サーバ、ラズパイ等を動かしている人などには一応使える物に仕上がっています。
　習作なのでデバッグ環境しか想定していませんが、適当にwsgiでnginxとかと繋いでやればOKでしょう。

　人間が書いたこのアプリケーションの説明
　このアプリケーションは、Python/FlaskによりWebユーザインタフェースでWoLを行うアプリケーションです。　DBとしてsqliteを使用します。
トップページにはFlaskルートへの一覧が表示されます。
リンクからアクセスして有用なのはregister_mac_address、send_magick_packet_routeとlist_machinesだけです。　それぞれ、マシン名からMACアドレスを取得してDBに保存する機能、MACアドレスを指定してマジックパケットを送信する機能、DBにあるマシン情報を一覧する機能を提供しています。
　register_mac_addressで起動中のLANマシン名を入力するとMACアドレスを探して、見つかればDBに追加します。　これが初期設定になるでしょう。
　後は、list_machinesページから操作する事になります。　マシン一覧が表示され、Wake Up/Edit/Deleteの三つのボタンが存在します。
　Wake Upはsend_magic_packet_routeにPOSTしてWoLを実行します。
　EditとDeleteはそのままですね。　Editはedit_machineにid付でアクセスして既存情報を編集します。　Edleteはdelete_machineにid付でPOSTするので確認無しにレコードは削除されます。　Copilotに頼んでこのボタンにJSで確認機能を付けて等してみるのも良さそうです。
　インストール方法はCopilotにお任せした物で問題ありません。

アップデート履歴
・初回
調整無しに取りあえず形が出来ただけの状態
・1回目
　Appを起動する部分がローカルしかリッスンしていないので、当該部分に移動してCopilotに修正して貰いました「全てのインタフェイスでリッスンして起動させて」
　リストからのWake Onリンクが誤っていたので直して貰いました（Wake On機能をリスト作った後に変更指示したのでそこが修正されていなかった）
　正直この修正は手書きの方が早いですが。
　そして、README.mdはCopilot生成の物でしたが、「日本語にして」とお願いした上で、このセクションを追加しました。
　なお、CommitのコメントもCopilotに任せたので今ひとつ的を射ない物になっていたりします。


# Flask マシン管理アプリケーション

これは、マシンを管理し、Wake-on-LAN (WoL) マジックパケットを送信してマシンを起動するための Flask ベースの Web アプリケーションです。このアプリケーションは、マシンの登録、登録されたすべてのマシンの一覧表示、マシンの詳細の編集、マシンの削除、および MAC アドレスによるマシンの起動のためのマジックパケットの送信機能を提供します。

## 機能

- **マシンの登録**: マシンの名前と MAC アドレスを登録します。
- **マシンの一覧表示**: 登録されたすべてのマシンの一覧を表示します。
- **マシンの編集**: 登録されたマシンの詳細を編集します。
- **マシンの削除**: 登録されたマシンを削除します。
- **マジックパケットの送信**: MAC アドレスによってマシンを起動するための Wake-on-LAN マジックパケットを送信します。

## Routes

- `/`: アプリケーション内のすべてのルートを一覧表示します。
- `/mac_regist`: マシンの名前と MAC アドレスを提供してマシンを登録します。
- `/wakeup_by_mac`: MAC アドレスによってマシンを起動するためのマジックパケットを送信します。
- `/edit_machine/<int:id>`: 登録されたマシンの詳細を編集します。
- `/delete_machine/<int:id>`: 登録されたマシンを削除します。
- `/machines`: 登録されたすべてのマシンを一覧表示します.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/studioes/copilot.git
    cd copilot
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    venv\Scripts\activate  # On Windows
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

4. Run the application:
    ```sh
    python main.py
    ```

## Usage

1. Open your web browser and navigate to `http://127.0.0.1:5000/`.
2. Use the provided forms to register machines, edit details, delete machines, and send magic packets.

## Code Overview

### `main.py`

- **Database Setup**: Configures and initializes the SQLite database using SQLAlchemy.
- **Machine Model**: Defines the `Machine` model with `id`, `name`, and `mac_address` fields.
- **Routes**:
  - `/`: Lists all available routes.
  - `/mac_regist`: Handles machine registration.
  - `/wakeup_by_mac`: Handles sending magic packets.
  - `/edit_machine/<int:id>`: Handles editing machine details.
  - `/delete_machine/<int:id>`: Handles deleting a machine.
  - `/machines`: Lists all registered machines.
- **Magic Packet Function**: Defines the `send_magic_packet` function to send a Wake-on-LAN magic packet.

### Example Code Snippet

```python
# MAC アドレスによってマシンを起動するためのマジックパケットを送信する関数
def send_magic_packet(mac_address):
    # ソケットオブジェクトを作成
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # ブロードキャストを許可するようにソケットオプションを設定
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    # マジックパケットを作成
    mac_bytes = bytes.fromhex(mac_address.replace(':', ''))
    magic_packet = b'\xff' * 6 + mac_bytes * 16

    # マジックパケットをブロードキャストアドレスに送信
    sock.sendto(magic_packet, ('<broadcast>', 9))

    # ソケットを閉じる
    sock.close()