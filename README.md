# 每日行情看板

每个交易日收盘后自动抓取美股数据,生成一个网页看板。跟踪 VOO、三大指数和观察列表。

## 部署步骤(不需要会用git,全程在网页上点)

1. 注册/登录 github.com,点右上角 + 号,选 New repository
   - 仓库名填 market-dashboard
   - 选 Public(必须是Public,免费版的Pages才能用)
   - 点 Create repository

2. 上传文件
   - 在新仓库页面点 uploading an existing file
   - 把 index.html、fetch_data.py、data.json 三个文件拖进去
   - 点 Commit changes
   - .github/workflows/update.yml 这个文件要单独建:点 Add file > Create new file,
     文件名输入 .github/workflows/update.yml(输入斜杠会自动建文件夹),
     把 update.yml 的内容粘贴进去,Commit changes

3. 开启网站
   - 仓库页面点 Settings > Pages
   - Source 选 Deploy from a branch,Branch 选 main,文件夹选 /(root),Save
   - 等一两分钟,页面上方会出现你的网址,形如
     https://你的用户名.github.io/market-dashboard/

4. 跑第一次数据
   - 仓库页面点 Actions 标签,如果提示启用workflows就点启用
   - 左边选「每日更新行情数据」,右边点 Run workflow
   - 跑完后刷新你的网站,示例数据就会变成真实行情

之后每个交易日收盘后(加州时间下午2点半左右)会自动更新,不用管。

## 想改跟踪的股票

编辑 fetch_data.py 最上面的 TICKERS 字典,加一行即可,比如:

    "MSFT": ("微软", "watch"),

改完等下一次自动运行,或去 Actions 手动跑一次。
