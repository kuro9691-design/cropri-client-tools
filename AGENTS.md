# 共通の操作ルーティング

外部アプリやWebサービスを扱うときは、対象に合った経路を最初から選ぶ。

1. 専用コネクタ／MCPが利用できる場合は最優先する。
   - 例: Gmail、Google Drive、Google Calendar、Notion。
2. ログイン済みChrome上のWebサービスはChrome連携を優先する。
   - 例: Facebook／Messenger、freee、WordPress管理画面、各種Web管理画面。
   - 汎用のComputer Useから開始しない。
3. WindowsのネイティブアプリはComputer Useを使う。
   - 例: LINE、Illustrator、CapCut。
   - LINEの確認依頼ではChromeを使わず、LINEデスクトップアプリを直接対象にする。
4. 公開情報の調査だけならWeb検索を使う。
5. 内蔵Browserは、公開サイトの閲覧や独立したブラウザ環境が適する場合に使う。

## cropri関連

- ホームページ制作・リニューアルは、ローカルファイル、コード、WordPress、既存の開発手順を中心に進める。
- ブラウザ上の表示確認やWordPress管理画面の操作が必要な場合のみChrome連携を使う。
- 現在問題なく動いている制作手順を、アプリ操作ルーティングのために変更しない。

## メッセージング

- Facebook／MessengerはChrome連携で確認する。
- LINEはLINEデスクトップアプリをComputer Useで確認する。
- 読み取り・要約のみの依頼では、返信やリアクションなどの変更を行わない。
- メッセージ送信は外部への代理通信になるため、文面を準備した後、送信直前にユーザー確認を取る。


## 情報の読み分け
- AIが検索・参照する本文は、実体のある `.md` を優先する。`.gdoc` はGoogleドキュメントへの参照ファイルであり、本文として扱わない。
- 同名の `.md` と `.md.gdoc` がある場合、通常作業では `.md` を読む。Googleドキュメント側の更新確認や再同期が必要な場合だけ専用コネクタで原本を読む。
- 事実や判断軸を AGENTS.md / CLAUDE.md に重複して書かない。ここには参照先と、そのプロジェクトに必要な安全ルールだけを書く。

## 作業時間
- 作業の開始時・区切りごと・終了時に、作業時間を記録する。後から推測で埋めない。
- 記録ツール: `C:\Users\user\.codex\cross-agent-handoff\cropri\work_time.py`（記録先は同じフォルダの work_time.json）
  - 共通の書き方（`--dir` は毎回必須）: `python "C:\Users\user\.codex\cross-agent-handoff\cropri\work_time.py" <コマンド> --dir "C:\Users\user\.codex\cross-agent-handoff\cropri" --actor <claude|codex> ...`
  - 開始: `start --task-id "cropriクライアント" --activity "作業内容"`
  - 区切り（意味のある操作・進捗ごと）: `heartbeat --activity "内容"`
  - 席を外す／戻る: `pause` ／ `resume`
  - 終了: `stop`
  - 集計: `report`（担当者・作業ID別の秒数。`--actor` は不要）
- Claude Code は `--actor claude`、Codex は `--actor codex`。人の作業時間を残すときだけ `--actor human` で手動記録する。
- 5分を超える空白は実働に入らない（ツールが自動で idle 扱いにする）。同じ担当者で2つの作業を同時に計測しない。
- 合計が必要なときだけ、PROGRESS.md に「作業時間の合計」を短く書く（記録そのものは work_time.json）。
