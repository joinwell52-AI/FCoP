<p align="center">
  <img src="assets/fcop-logo-256.png" alt="FCoP Logo" width="180" />
</p>

<h1 align="center">FCoP 鈥?鏂囦欢椹卞姩鐨?Agent 鍗忎綔鍗忚</h1>

<p align="center">
  <em>澶?Agent 鍗忎綔涓殑<strong>琛屼负娌荤悊鍗忚灞?/strong>鈥斺€旇鑼?Agent 濡備綍鎶ュ憡琛屼负銆佸闃呯粨鏋滃苟鍦ㄥ彈娌荤悊鐨勮兘鍔涜竟鐣屽唴杩愪綔銆?/em><br/>
  <strong>鏍稿績涓嶅彉閲忥細<code>Filename as Protocol</code>锛堟枃浠跺悕鍗冲崗璁級路鏂囦欢澶瑰氨鏄秷鎭€荤嚎</strong>
</p>

<p align="center">
  <strong><a href="https://joinwell52-ai.github.io/FCoP/">馃寪 椤圭洰涓婚〉</a></strong> 路
  <a href="README.md">English</a> 路
  <a href="docs/getting-started.md">涓婃墜 FCoP</a> 路
  <a href="src/fcop/rules/_data/agent-install-prompt.zh.md"><strong>馃憠 璁?AI 瀹夎锛?/strong></a> 路
  <a href="src/fcop/rules/_data/agent-bringup-prompt.zh.md"><strong>馃憠 璁?AI 璧烽」鐩紒</strong></a> 路
  <a href="docs/mcp-tools.md"><strong>MCP 宸ュ叿娓呭崟锛?5 涓級</strong></a> 路
  <a href="essays/when-ai-organizes-its-own-work.md">鐜板満鎶ュ憡</a> 路
  <a href="essays/fcop-natural-protocol.md">鑷劧鍗忚</a> 路
  <a href="spec/fcop-3.0-spec.zh.md"><strong>3.0 瑙勮寖锛堜腑鏂囷級</strong></a> 路
  <a href="adr/README.md">ADR 绱㈠紩</a>
</p>

<p align="center">
  <a href="https://dev.to/joinwell52/we-replaced-our-multi-agent-middleware-with-a-folder-48-hours-later-the-ai-invented-6-42a9">
    <img src="https://img.shields.io/badge/DEV-%E9%95%BF%E6%96%87%E5%AE%A2%E6%A0%88-black?style=flat-square&logo=dev.to&logoColor=white" alt="DEV Community 闀挎枃" />
  </a>
  <a href="https://forum.cursor.com/t/fcop-let-multiple-cursor-agents-collaborate-by-filename-mit-0-infra/158447">
    <img src="https://img.shields.io/badge/Cursor%20%E8%AE%BA%E5%9D%9B-%E8%AE%A8%E8%AE%BA-0066FF?style=flat-square" alt="Cursor 绀惧尯璁哄潧" />
  </a>
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/license-MIT-blue?style=flat-square" alt="MIT License" />
  </a>
  <a href="CHANGELOG.md">
    <img src="https://img.shields.io/badge/%E5%8F%91%E5%B8%83-3.2.3-brightgreen?style=flat-square" alt="3.2.3" />
  </a>
  <a href="spec/fcop-3.0-spec.zh.md">
    <img src="https://img.shields.io/badge/%E8%A7%84%E8%8C%83-FCoP%203.0-orange?style=flat-square" alt="FCoP 3.0 瑙勮寖" />
  </a>
  <a href="https://registry.modelcontextprotocol.io/v0/servers?search=io.github.joinwell52-AI%2Ffcop">
    <img src="https://img.shields.io/badge/MCP%20%E6%B3%A8%E5%86%8C%E8%A1%A8-io.github.joinwell52--AI%2Ffcop-8A2BE2?style=flat-square" alt="瀹樻柟 MCP 娉ㄥ唽琛?io.github.joinwell52-AI/fcop" />
  </a>
  <a href="https://doi.org/10.5281/zenodo.19886036">
    <img src="https://zenodo.org/badge/DOI/10.5281/zenodo.19886036.svg" alt="DOI 10.5281/zenodo.19886036" />
  </a>
</p>

---

## 馃啎 FCoP 3.0 宸插彂甯冣€斺€?鏂囦欢鍗冲崗璁紱浣嶇疆瀹氫箟鐘舵€侊紱浜嬩欢璁板綍鍘嗗彶銆?

<p align="center">
  <a href="spec/fcop-3.0-spec.zh.md">
    <img src="assets/fcop-3.0-architecture.zh.png" alt="FCoP 3.0 路 浣撶郴缁撴瀯鍏ㄦ櫙鍥锯€斺€旀枃浠跺嵆鍗忚锛涗綅缃畾涔夌姸鎬侊紱浜嬩欢璁板綍鍘嗗彶銆? width="900" />
  </a>
</p>

> **FCoP 3.0** 鏄崗璁殑绗竴娆?*璇箟灏佹澘**銆傜姸鎬佷綇杩涙枃浠剁郴缁熸湰韬紙`_lifecycle/{inbox,active,review,done,archive}/`锛夛紝浜嬩欢浠ュ彧杩藉姞鏂瑰紡浣忓湪鏂囦欢鍐呴儴锛岃€?*custody / ownership / scheduling / runtime* 琚樉寮忓垝鍒?*鍗忚涔嬪**锛圔oundary Charter锛夈€?
>
> 浠?2.x 鍗囩骇璇疯繍琛?`python -m fcop migrate --to-v3`銆?

| 鏂囨。 | 鐢ㄩ€?|
|---|---|
| [`spec/fcop-3.0-spec.zh.md`](spec/fcop-3.0-spec.zh.md) 路 [en](spec/fcop-3.0-spec.md) | 涓枃鍗曢〉姝ｅ紡瑙勮寖 |
| [`spec/fcop-3.0-rfc.zh.md`](spec/fcop-3.0-rfc.zh.md) 路 [en](spec/fcop-3.0-rfc.md) | RFC 涓枃骞宠鐗?|
| [`docs/MIGRATION-3.0.zh.md`](docs/MIGRATION-3.0.zh.md) 路 [en](docs/MIGRATION-3.0.md) | 2.x 鈫?3.0 杩佺Щ鎸囧崡 |
| [`CHANGELOG.md` `[3.0.0]`](CHANGELOG.md) | 瀹屾暣 release notes |
| [`essays/the-day-we-almost-added-custody.md`](essays/the-day-we-almost-added-custody.md) 路 [en](essays/the-day-we-almost-added-custody.en.md) | 瀹氫箟 3.0 鐨勯偅娆″喅绛?|

---

## FCoP 鍦ㄦ妧鏈爤涓殑浣嶇疆

FCoP 鏄 Agent 鍗忎綔涓殑**琛屼负娌荤悊鍗忚灞?*鈥斺€旇鑼?Agent 濡備綍鎶ュ憡琛屼负銆佸闃呯粨鏋滃苟鍦ㄥ彈娌荤悊鐨勮兘鍔涜竟鐣屽唴杩愪綔銆?

```
搴旂敤灞?         CodeFlow / Cursor / Claude Desktop       鈫?涓氬姟浜у搧 / Agent 搴旂敤
瀹夸富閫傞厤灞?     fcop-mcp / fcop-cli / @fcop/claude       鈫?闆嗘垚閫傞厤鍣?/ 瀹夸富妗ユ帴灞?
鈽?FCoP 鍗忚灞?鈽?Agent 鍗忎綔 / 琛屼负鎶ュ憡 / Review /         鈫?FCoP 鐨勬牳蹇冭亴璐?
                Capability Governance / 浜嬩欢璇箟 /
                澶辫触杈圭晫 / 瀹¤鑳藉姏
鍙傝€冨疄鐜板眰      fcop锛圥ython Library锛?                  鈫?FCoP 鍗忚鐨勫弬鑰冨疄鐜?
鎵ц鍩哄簳灞?     LLM APIs / MCP 宸ュ叿 / 鏂囦欢绯荤粺 /         鈫?鎵ц鐜锛團CoP 涓嶆嫢鏈夛級
                杩涚▼绠＄悊 / 鎿嶄綔绯荤粺
```

> **FCoP 娌荤悊 Agent 琛屼负锛岃€岄潪鎵ц杩愯鏃躲€?* 鈥斺€?[ADR-0029](adr/ADR-0029-fcop-behavior-governance-charter.md)

v1.0 灏嗕竷澶ф牳蹇冩蹇碘€斺€?*Agent銆丒ncoding銆両PC銆丒vent銆丗ailure銆丅oundary銆丄udit**鈥斺€旂殑鏈€灏忚涔夊绾︽寮忓浐鍖栦负绋冲畾鏍囧噯銆俿pec 鍥哄寲銆乪ncoding 鐣欑櫧锛?IPC Surface*锛圱ASK / REPORT / ISSUE / REVIEW锛夊己绫诲瀷锛?Open Knowledge Surface*锛坄shared/` + `{ALL-CAPS-PREFIX}-{slug}.md`锛夎瘝琛ㄥ畬鍏ㄥ紑鏀撅紝璁?agent 鑷敱鍙戞槑鈥斺€旇 [ADR-0021](adr/ADR-0021-encoding-abstraction.md)銆?

鈫?**浠庤繖閲屽紑濮?*锛歔`docs/getting-started.md`](docs/getting-started.md) 路 [`docs/getting-started.en.md`](docs/getting-started.en.md)

---

## 涓€鍙ヨ瘽璇存竻妤?

涓绘祦鐨勫 Agent 妗嗘灦瑕侀潬娑堟伅闃熷垪銆佹暟鎹簱銆佽嚜鐮?RPC 涓棿浠躲€侳CoP 鍏ㄩ儴鎵旀帀锛屽彧鐣?*鏂囦欢绯荤粺**锛?

- **鐩綍灏辨槸鐘舵€併€?*`tasks/` / `reports/` / `issues/` / `log/`锛屾枃浠朵粠涓€涓洰褰?`rename` 鍒板彟涓€涓氨鏄姸鎬佹祦杞€?
- **鏂囦欢鍚嶅氨鏄矾鐢便€?*`TASK-20260418-001-PM-to-DEV.md` 涓€鐪肩湅寰楀嚭鍙戜欢浜恒€佹敹浠朵汉銆佺被鍨嬨€佹祦姘村彿銆?
- **鍐呭灏辨槸璐熻浇銆?*Markdown + 涓€鐐圭偣 YAML frontmatter锛孉gent 鍜屼汉璇诲啓鐨勬槸鍚屼竴浠戒笢瑗裤€?
- **鍞竴鐨勫悓姝ュ師璇槸 `os.rename()`銆?*POSIX 鍦ㄥ悓涓€鎸傝浇鐐瑰唴淇濊瘉瀹冨師瀛愨€斺€斾笉闇€瑕侀攣銆佷笉闇€瑕?broker銆佷笉闇€瑕佸叡璇嗙畻娉曘€?

灏辫繖浜涖€傛病鏈夋暟鎹簱锛屾病鏈夋秷鎭槦鍒楋紝娌℃湁甯搁┗瀹堟姢杩涚▼銆傛暣涓郴缁熺姸鎬?`ls` 灏辫兘鐪嬪畬锛屾暣娈靛崗浣滃巻鍙?`git log` 灏辫兘鍥炴斁銆?

> 濡傛灉璇?TCP 鏄?瀛楄妭璺戝湪绾跨紗涓?锛?*FCoP 灏辨槸"浠诲姟璺戝湪鏂囦欢澶归噷"銆?*

> 鍦ㄥ伐绋嬩笂锛屽氨鏄敤**鍙簭鍒楀寲銆佸彲鐗堟湰鍖栫殑鍗忎綔闈?*锛屾崲璧颁簡瀵?*涓撳睘銆佹矇閲嶅熀纭€璁炬柦**鐨勪緷璧栥€?

## 涓轰粈涔堝€煎緱涓€鐪?

鍥犱负**鐪嬪緱瑙佺殑 Agent锛屾墠绠″緱浣忋€?*

鎴戜滑鐢ㄤ竴鏀?4 浜?AI 鍥㈤槦锛圥M / DEV / QA / OPS锛夎窇浜?48 灏忔椂锛孉gent 浠?*鑷彂鍙戞槑浜?6 绉嶆垜浠粠娌″啓杩涜鑼冪殑鍗忎綔妯″紡**鈥斺€斿叏浣撳箍鎾€佽鑹叉Ы浣嶃€佸叡浜枃妗ｃ€佸瓙浠诲姟鎵规銆佽嚜瑙ｉ噴 README銆佸彲杩芥函鎬?frontmatter銆傛瘡涓€绉嶆柊妯″紡閮借〃鐜颁负**鏂版枃浠跺悕**鈥斺€旀垜浠竴琛屼唬鐮侀兘娌℃敼銆?

鍚庢潵鍙堝嚭鐜颁簡鏇存剰澶栫殑涓€骞曪細涓€涓?*鍗曠嫭**鐨?agent锛屽湪涓€涓?*涓庝换浣曞綋鏃跺凡鎵撳紑鐨勯」鐩伐浣滃尯閮芥棤鍏?*鐨勬湰鍦扮洰褰曢噷锛堜緥濡傜敓鎴愪竴娈?AI 闊充箰瑙嗛锛夛紝**鑷彂**鎶婅嚜宸辨媶鎴?PM / DEV / ADMIN 涓変釜瑙掕壊銆佺粰鑷繁鍐欎簡鍥涗唤 FCoP 鏍煎紡鐨勫叕鏂囷紝杩?*鍗囧崕**浜嗘垜閭ｄ簺鍒嗘暎鍦?7 涓枃浠堕噷鐨勬妧鏈瀹氾紝娴撶缉鎴愪竴鍙ユ垜鏍规湰娌″啓杩囩殑鍘熷垯鎬х瑷€銆?

杩欎袱娈垫晠浜嬮兘鏁寸悊鎴愪簡鐜板満鎶ュ憡锛岃涓嬮潰鐨勬枃绔犵储寮曘€?

## 鐜板満鎶ュ憡 路 Essays

| # | 鏍囬 | 鐗堟湰 | 涓€鍙ヨ瘽 |
|---|---|---|---|
| 01 | **褰?AI 鑷繁鏁寸悊宸ヤ綔** | [GitHub 涓枃](essays/when-ai-organizes-its-own-work.md) 路 [CSDN](https://blog.csdn.net/m0_51507544/article/details/160344932) 路 [English](essays/when-ai-organizes-its-own-work.en.md) | 涓€鏀?4 浜?AI 鍥㈤槦锛圥M / DEV / QA / OPS锛夛紝48 灏忔椂锛屽彧缁欎竴涓枃浠跺す鈥斺€旂粨鏋滆嚜鍙戞秾鐜板嚭 6 绉嶆垜浠粠娌″啓杩涜鑼冪殑鍗忎綔妯″紡銆?|
| 02 | **涓€涓棤娉曞畬鍏ㄨВ閲婄殑鐜拌薄:AI 涓嶆鏈嶄粠瑙勫垯,瀹冭鍚岃鍒?* | [GitHub 涓枃](essays/fcop-natural-protocol.md) 路 [GitHub English](essays/fcop-natural-protocol.en.md) 路 [CSDN 涓枃](https://blog.csdn.net/m0_51507544/article/details/160345043) 路 [Dev.to](https://dev.to/joinwell52/an-unexplainable-thing-i-saw-the-agent-didnt-just-comply-with-rules-it-endorsed-them-5ecd) 路 [Cursor Forum](https://forum.cursor.com/t/i-asked-cursor-to-make-a-video-it-wrote-itself-4-protocol-memos-field-report-on-rule-internalization/158524) | 涓€涓?agent 鍦?*瀹屽叏鏃犲叧**鐨勪换鍔￠噷锛岃嚜鍙戞妸鑷繁鎷嗘垚 4 涓?FCoP 瑙掕壊锛岃繕**鍗囧崕**浜嗘垜鏁ｅ湪 7 涓枃浠堕噷鐨勬妧鏈瀹氾紝娴撶缉鎴愪竴鏉℃垜鏍规湰娌″啓杩囩殑鍘熷垯銆傞檮[瀹屾暣璇佹嵁妗ｆ](essays/fcop-natural-protocol-evidence/)锛? 寮犳埅鍥?+ 4 浠藉叕鏂?+ 鍘熷 JSONL 杞綍锛夈€?|
| 03 | **鑷劧鍗忚涓轰粈涔堢珯寰椾綇鈥斺€擣CoP 浠?TMPA 涓娊鍑烘潵鐨勯偅鏉′鸡鐞?* | [GitHub 涓枃](essays/fcop-tmpa-lineage.md) 路 [GitHub English](essays/fcop-tmpa-lineage.en.md) | 02 鐨勫濡圭瘒銆傞偅涓€绡囪"杩欎欢浜嬪彂鐢熶簡"锛岃繖涓€绡囪"瀹冧负浠€涔堢珯寰椾綇"锛欶CoP 鍏跺疄鏄粠 **TMPA**锛堜竴浠藉 AI 鏋舵瀯瑙勮寖锛屾牳蹇冪珛鎰忔槸鐢ㄧ函鏂囨湰鏃跺簭鏇夸唬浼犵粺鍒嗗竷寮忓崗璋冿級閲屾娊鍑烘潵鐨勫瓙闆嗭紱agent 鍗囧崕鍑虹殑閭ｅ彞璇濓紝鏄?TMPA 浼︾悊灞?澶氳鑹插鏍告槸 AI 浼︾悊寮哄埗"鐨勬渶灏忓寲閲嶅彂鐜般€?|
| 04 | **璁?agent 璇?涓?锛屾槸 LLM 鏈€闅惧仛鐨勪簨鈥斺€擣CoP 缁欎簡瀹冭娉?* | [GitHub 涓枃](essays/when-ai-vacates-its-own-seat.md) 路 [GitHub English](essays/when-ai-vacates-its-own-seat.en.md) 路 [鐜板満璇佹嵁妗ｆ](essays/when-ai-vacates-its-own-seat-evidence/INDEX.md) 路 [CSDN 涓枃](https://blog.csdn.net/m0_51507544/article/details/160513899) 路 [Dev.to](https://dev.to/joinwell52/saying-no-is-the-hardest-thing-for-an-llm-fcop-gives-it-grammar-3ccd) 路 [Cursor Forum](https://forum.cursor.com/t/saying-no-is-the-hardest-thing-for-an-llm-fcop-gives-it-grammar/159037) | 鍚屼竴鍙扮數鑴戙€佷袱涓?Cursor 浼氳瘽銆佷袱涓?GPT-5 灏忕増鏈紙5.4 涓?5.5锛夛細鍘?PM 鍦ㄦ垜璇?鎵句簡涓存椂 PM"鍚庝富鍔ㄨ鍑哄腑浣嶅洖鍒?UNBOUND锛屾柊 PM.TEMP 鐢ㄣ€宖rontmatter 闄嶇骇 + 姝ｆ枃 `璇存槑:` 涓€琛屻€嶈蛋瀹屼簡鍗忚娌″啓鐨勯偅鏉¤矾銆傛垜鍘熸湰浠ヤ负浼氬啿绐侊紝缁撴灉娌℃湁鈥斺€攁gent 鑷繁鎶婅鍒欒ˉ鍏ㄤ簡銆傞檮 15 寮犳埅鍥?+ 2 浠藉畬鏁?JSONL 杞綍銆?|
| 05 | **鏁欑▼锛歴olo 鍗?agent 杞?2 浜哄洟闃熲€斺€擣CoP-MCP 璁?AI 鍥㈤槦鏈夌邯寰?*锛堜袱涓苟鍒楁渚嬶級 | 涓枃姣嶈鍘熷垱锛堣椽鍚冭泧妗堜緥锛? [`snake-solo-to-duo.zh.md`](docs/tutorials/snake-solo-to-duo.zh.md) 路 [CSDN](https://blog.csdn.net/m0_51507544/article/details/160603953) 路 English (Tetris case): [`tetris-solo-to-duo.en.md`](docs/tutorials/tetris-solo-to-duo.en.md) 路 [Dev.to](https://dev.to/joinwell52/free-open-source-multi-agent-hands-on-how-to-command-agents-fcop-mcp-brings-discipline-to-1j3j) 路 [Cursor Forum](https://forum.cursor.com/t/free-open-source-multi-agent-hands-on-how-to-command-agents-fcop-mcp-brings-discipline-to-ai-teams/159329) 路 涓枃璇戞湰锛堜縿缃楁柉鏂瑰潡妗堜緥锛? [`tetris-solo-to-duo.zh.md`](docs/tutorials/tetris-solo-to-duo.zh.md) | 鍞竴涓€绡?*鏁欑▼鎬ц川**鐨勬枃绔狅紝浠?*涓や釜骞跺垪妗堜緥**褰㈠紡鍙戝竷鈥斺€?*鍗忚鐩稿悓锛屾渚嬫父鎴忎笌鐜板満褰╄泲涓嶅悓**銆備袱涓渚嬮兘鏄?45 鍒嗛挓璺熺湡瀹?dogfood 璧颁竴閬嶏細璁?AI 鏇夸綘瑁?`fcop-mcp`锛宻olo 鍐欎竴鍙兘璺戠殑灏忔父鎴忥紝涓€鍙ヨ瘽鍒?2 浜哄洟闃熷悗 PLANNER 璁捐 + CODER 瀹炵幇鍒涙剰鍙樹綋锛屾渶鍚庤鐩樼湅瀹屾暣璐︽湰銆?*涓枃妗堜緥**鐢ㄨ椽鍚冭泧 鈫?鍘熷垱涓婚銆婃槦杞ㄧ粐鑰?NEON ORBIT銆嬶紝闄?18 寮犳埅鍥?+ 涓€娆＄湡瀹炵殑 PLANNER 瓒婄晫鍐掑厖 CODER 褰╄泲锛?.6.x 鏃朵唬鐨勫崗璁秺鐣岃瘉鎹級銆?*鑻辨枃妗堜緥**鐢ㄤ縿缃楁柉鏂瑰潡 鈫?鍗曚汉銆奛ebula Stack銆嬧啋 鍙屼汉銆奀omet Loom銆嬶紝澶氫簡涓€涓湡瀹炵殑"璇勫 鈫?鎷掓敹 鈫?閲嶅仛"寰幆锛坴1 琚?ADMIN 璇曠帺椹冲洖锛孭LANNER 鍐?TASK-006 鍔?`Verification Requirements`锛寁2 閫氳繃锛? 褰撳満璁胯皥涓や釜 agent "浣犳€庝箞鐪?FCoP" 鏀跺埌鐨勮瘹瀹炶嚜璇勩€備袱涓渚嬪叡 22 寮?dogfood 鎴浘銆?4 浠?TASK/REPORT銆? 浠?role-switch 闈欓粯璇佹嵁銆? 浠芥父鎴忎唬鐮併€? 浠?verbatim agent 璁胯皥 transcript鈥斺€斿叏閮ㄥ綊妗ｅ湪 [`docs/tutorials/assets/tetris-en/`](docs/tutorials/assets/tetris-en/)銆?|
| 06 | **鐩存帴闂?agent 瀹冩€庝箞鐪?FCoP鈥斺€斿畠璇村嚭浜嗘垜浠病璁╁畠璇寸殑璇?* | [GitHub 涓枃](essays/what-agents-say-about-fcop.md) 路 [GitHub English](essays/what-agents-say-about-fcop.en.md) 路 [鐜板満璇佹嵁锛堜縿缃楁柉鏂瑰潡妗堜緥 dogfood锛塢(docs/tutorials/assets/tetris-en/) 路 [CSDN 涓枃](https://blog.csdn.net/m0_51507544/article/details/160636177) 路 [Dev.to](https://dev.to/joinwell52/what-the-agents-say-about-fcop-when-you-ask-them-3ajk) 路 [Cursor Forum](https://forum.cursor.com/t/what-the-agents-say-about-fcop-when-you-ask-them-two-field-interviews-at-the-end-of-an-english-dogfood/159368) | 绗笁绫?agent 鍙嶅悜璁ゅ悓 FCoP"鐨勮瘉鎹€斺€斿湪 [essay 02](essays/fcop-natural-protocol.md)锛?*鑷彂瑙﹀彂锛屾棤鍏充换鍔?*锛夊拰 [essay 04](essays/when-ai-vacates-its-own-seat.md)锛?*琚啿绐侀€煎嚭鏉?*锛変箣鍚庯紝杩欐鐨勮Е鍙戞潯浠舵槸**琚洿鎺ラ棶**銆備竴娆¤嫳鏂囦縿缃楁柉鏂瑰潡 dogfood 鏀跺熬鏃讹紙鏁欑▼琛?05 鐨勪即闅?essay锛夛紝鎴戝垎鍒湪涓や釜浼氳瘽閲岄棶 PLANNER 鍜?CODER 鍚屼竴绫婚棶棰樷€斺€攁gent 瑙嗚鐨勮€佸疄璇濓紝鏃犺惀閿€鑵斻€侾LANNER 鎶?"follow latest instruction" 杩欎釜 RLHF 璁嚭鏉ョ殑鏈兘鍛藉悕涓鸿嚜宸变负浜嗗畧浣?FCoP 瑙掕壊閿侀渶瑕?瀵规姉"鐨勯偅涓€闈紝鎶婂畠鍚嶄笅浜х敓鐨?8 浠?`role-switch` 璇勫畾涓?*鐪熼槼鎬?*鑰屼笉鏄鎶ャ€侰ODER 鎵胯 TASK-003 鏈夎鏍兼紡娲?+ **鍗忚鏈潵缁欎簡瀹冧竴鏉?pushback 璺緞锛坄write_issue`锛夊畠娌＄敤**鈥斺€攙1 缂洪櫡姝ｅソ闀垮湪閭ｅ潡娌¤鐩栫殑绌虹櫧涓娾€斺€斿苟缁欏嚭 PR 绾у埆鐨勫崗璁骇鍝佸弽棣堛€備笁绉嶈Е鍙戞潯浠讹紝鍚屼竴涓幇璞★細**鍙缁欑┖闂达紝agent 灏变細鍙嶈繃鏉ヨ鍚?FCoP**銆傝繕鏈変竴涓?dogfood 椤哄甫浜у嚭鐨勫皬瑙傚療鍊煎緱鐣欏簳鈥斺€旀暣鏁?45 鍒嗛挓锛孉DMIN 璇村緱鏈€澶氱殑涓ゅ彞璇濇槸 **"Start work."** 鍜?**"Inspection."** |
| 07 | **褰?agent 浠庤嚜宸辩殑娈嬮涓涔?* | [GitHub 涓枃](essays/when-agents-learn-from-their-own-wreckage.md) | codeflow 椤圭洰涓€鏃?14 涓?agent 娑岀幇鐜板満鎶ュ憡锛?026-05-12锛夛細USER HOME 鍏ㄥ眬姹℃煋 / GATE 鎻忚堪鑷懡涓?/ `supersedes:` 瀛楁鐜板満鍙戞槑鈥斺€斾互鍙婂崗璁浣曞湪闆舵宕╂簝鐨勬儏鍐典笅锛屼互灏忔椂绾ч€熷害灏嗗畠浠叏閮ㄥ弽鍚戝惛鏀躲€?|
| 08 | **鍗忚涓轰粈涔堢煭锛屽巻鍙蹭负浠€涔堥暱** | [GitHub 涓枃](essays/why-the-protocol-stays-short.md) | 涓€浠界粰鍗忚缁存姢鑰呯殑璁捐鍝插绛旀锛?杩欐牱鐨勬秾鐜颁細涓嶄細娌℃湁姝㈠锛?鈥斺€旂煭绛旓細浼氭敹鏁涗絾涓嶄細鍋溿€傚洓绫绘秾鐜扮殑澶勭悊璺緞銆佷笁鏉＄粨鏋勫姏瀛︿负浣曡兘璁╁崗璁鏋朵笉琚秾鐜板帇鍨紝浠ュ強"鍗忚鐭槸涓轰簡璁╁巻鍙茶兘鏃犻檺闀?鐨勫簳灞傞€昏緫銆?|
| 09 | **褰?validator 鎾炲悜鑷繁鐨勯暅鍍?* | [GitHub 涓枃](essays/gate-design-pitfalls-case-studies.md) | 浠?codeflow OPS I-14 鐪?validator-validates-itself 鍙嶆ā寮忥細GATE 鍦ㄦ鏌?staged diff 鏃跺懡涓簡 GATE 鎻忚堪鏈韩锛屽嚑鍒嗛挓鍚庤 OPS 鑷籂鈥斺€旇繖涓€绫婚櫡闃辩殑绯荤粺鎬цВ鍓栦笌"璇箟鍖栧疄璇?鏍规不濮垮娍锛屼互鍙婂畠濡備綍鎴愪负 `fcop-protocol.mdc 搂GATE Design Pitfalls` 鐨勬簮澶存渚嬨€?|
| 10 | **涓€琛?frontmatter 鐨勬梾绋?* | [GitHub 涓枃](essays/the-supersedes-field-story.md) | `supersedes:` 瀛楁浠庝竴娆″崗璁袱闅剧幇鍦哄彂鏄庡埌 `ipc-envelope.schema.json` 姝ｅ紡瀛楁鐨勪袱灏忔椂鏃呯▼锛歊ule 5锛坅ppend-only锛? Rule 6锛坮eciprocity锛? Rule 0.c锛坱ruthful锛変笁鏉¤鍒欏悓鏃舵垚绔嬫椂锛宎gent 鐢ㄤ竴琛?YAML 鑷繁瑙ｄ簡鍥板眬鈥斺€旇繖鏉¤矾寰勫睍绀?FCoP 娑岀幇钀藉湴鐨勬渶浣庢垚鏈Э鍔裤€?|
| 11 | **鐪嬶紝浣嗕笉鍔ㄦ墜** | [GitHub 涓枃](essays/looking-without-touching.md) | FCoP 涓夊眰璇箟鎵ц閾剧鏅細`fcop_audit()` 涓轰粈涔?鍙湅涓嶆敼"鈥斺€擫1 妫€娴?/ L2 瑙ｉ噴 / L3 鏂囨。涓夊眰鎶?鐪嬭"鍜?鍔ㄦ墜"鍒囧紑锛屼骇鍑?`INSPECTION.md`锛堝缓璁潪鍛戒护锛夛紝鎵ц鏉冪暀缁欎汉銆俙adr/FCoP-semantic-execution-chain.md` 鐨勭鏅増銆?|
| 12 | **浜斿ぇ AI 妯″瀷鐪间腑鐨?FCoP** | [GitHub 涓枃](essays/what-five-ai-models-say-about-fcop.md) 路 [GitHub English](essays/what-five-ai-models-say-about-fcop.en.md) | 鎶?FCoP 鏍稿績鏂囨。鍠傜粰 ChatGPT / Claude / DeepSeek / Grok / 璞嗗寘锛屽彧闂竴涓棶棰橈細"浣犳槸 agent锛屼綘鎬庝箞鐪嬭繖濂楀崗璁紵"鈥斺€斾簲绉嶆埅鐒朵笉鍚岀殑鍐呴儴瑙嗚锛圕hatGPT 璋堣韩浠藉悎娉曟€с€丆laude 璋堣瘹瀹炶竟鐣屻€丏eepSeek 璋堜綋闈㈢敓瀛樸€丟rok 鍋氭妧鏈瘎瀹°€佽眴鍖呰璁捐鍝插锛夛紝浠ュ強瀹冧滑涔嬮棿鏈€鏈夋剰鎬濈殑鍒嗘銆?|
| 13 | **婕斿寲锛屽弽鍚戝惛鏀?* | [GitHub 涓枃](essays/evolution-reverse-absorption.md) 路 [GitHub English](essays/evolution-reverse-absorption.en.md) | 鍗忚鍝插 2.0 瑙嗚瀹ｈ█锛欶CoP 浠庡崟寮犳墽琛屽摬瀛﹀浘锛?鐪嬶紝浣嗕笉鍔ㄦ墜"锛夎繘鍏?*涓ゅ紶鍥惧叡鍚屽畾涔?*鏃朵唬鈥斺€旀柊澧炴紨鍖栧摬瀛﹀浘锛? 姝ヨ涔夋紨鍖栭棴鐜級涓庨厤濂?[ADR-0034](adr/ADR-0034-fcop-internal-external-document-convention.md)锛屾妸 4 灞傛秾鐜版ā寮?/ 鍐呭鏂囨。绾﹀畾 / 鍙嶅悜鍚告敹鏈哄埗鍐欏叆鍗忚銆俥ssay 11 鐨勫鐢熷濡圭瘒銆?|
> 娆㈣繋鎻愪氦鏂扮殑鐜板満鎶ュ憡銆傚鏋滀綘鍦ㄨ嚜宸辩殑椤圭洰閲岀敤浜?FCoP锛岄亣鍒颁簡鎰忓锛堝ソ鎴栧潖锛夛紝娆㈣繋寮€ issue 鎴栧 `essays/` 鎻?PR銆傚崗璁槸鍦ㄧ幇鍦烘姤鍛婇噷婕旇繘鐨勶紝涓嶆槸鍦ㄥ鍛樹細閲屻€?

## 浠撳簱缁撴瀯

姒傝锛氭牴鐩綍闄?*鍗忚涓庢枃妗?*澶栵紝杩樻湁 **PyPI `fcop` 鐨勬簮鐮?*锛坄src/fcop/`锛変笌**鐙珛瀛愰」鐩?`fcop-mcp`**锛坄mcp/`锛夛紝浠ュ強娴嬭瘯涓庡彂鐗?ADR 鏀拺鐩綍銆?

```
FCoP/
鈹溾攢鈹€ src/fcop/                    # `fcop` 鍖咃細Project 绛夊簱 API锛沗rules/_data/` 鍐呯疆 fcop-rules / fcop-protocol锛坕nit 鏃跺彲閫夐儴缃茬殑姣嶇増锛?
鈹溾攢鈹€ mcp/                         # `fcop-mcp` 瀛愰」鐩紙MCP 鏈嶅姟鍣紝鑷湁 pyproject锛?
鈹溾攢鈹€ tests/                       # `fcop` / `fcop-mcp` 鐨?pytest
鈹溾攢鈹€ spec/                        # 瑙勮寖鏂囦欢锛堝弬瑙?spec/README.md锛?
鈹?  鈹溾攢鈹€ fcop-3.0-spec.md         # 鈽?鑻辨枃鏉冨▉瑙勮寖锛團CoP 3.0 canonical锛?
鈹?  鈹溾攢鈹€ fcop-3.0-spec.zh.md      # 涓枃骞宠鐗堬紙informative锛?
鈹?  鈹溾攢鈹€ fcop-3.0-rfc.md / .zh.md # IETF 椋庢牸 RFC 鐗堟湰
鈹?  鈹溾攢鈹€ schemas/                 # 8 JSON Schemas锛堟満鍣ㄥ彲璇伙級
鈹?  鈹斺攢鈹€ archived/                # v1.0 / v1.1 / 0.7.x 鏃╂湡 spec锛堝凡琚彇浠ｏ紝淇濈暀浣滃巻鍙诧級
鈹溾攢鈹€ docs/                        # 鍏ラ棬銆佽縼绉汇€佸彂鐗堣褰曘€丮CP 宸ュ叿璇存槑
鈹?  鈹斺攢鈹€ getting-started.md      # 鈫?鏂扮敤鎴蜂粠杩欓噷寮€濮?
鈹溾攢鈹€ adr/                         # 鏋舵瀯鍐崇瓥锛圓DR-0001..0022锛?
鈹溾攢鈹€ .github/workflows/           # CI
鈹溾攢鈹€ pyproject.toml               # 鏍?`fcop` 鍖呬笌宸ュ叿閰嶇疆
鈹溾攢鈹€ essays/
鈹?  鈹溾攢鈹€ when-ai-organizes-its-own-work.md
鈹?  鈹溾攢鈹€ when-ai-organizes-its-own-work.en.md
鈹?  鈹溾攢鈹€ fcop-natural-protocol.md
鈹?  鈹溾攢鈹€ fcop-natural-protocol.en.md
鈹?  鈹溾攢鈹€ fcop-natural-protocol-evidence/
鈹?  鈹溾攢鈹€ fcop-tmpa-lineage.md
鈹?  鈹溾攢鈹€ fcop-tmpa-lineage.en.md
鈹?  鈹溾攢鈹€ when-ai-vacates-its-own-seat.md
鈹?  鈹溾攢鈹€ when-ai-vacates-its-own-seat.en.md
鈹?  鈹溾攢鈹€ when-ai-vacates-its-own-seat-evidence/
鈹?  鈹溾攢鈹€ what-agents-say-about-fcop.md
鈹?  鈹斺攢鈹€ what-agents-say-about-fcop.en.md
鈹溾攢鈹€ examples/workspace-example/  # 鏈€灏忓弬鑰冨伐浣滃尯
鈹溾攢鈹€ integrations/windows-file-association/
鈹溾攢鈹€ assets/                      # Logo
鈹溾攢鈹€ LICENSE
鈹斺攢鈹€ README.md / README.zh.md
```

## 30 绉掑揩閫熶笂鎵?

FCoP 鏄€岄噰绾炽€嶅崗璁紝涓嶆槸瑁呬竴涓嫭绔嬪畧鎶よ繘绋嬨€傚綋鍓嶇増鏈殑**瑙勮寖渚?*鏄垚瀵圭殑 **[鎬诲垯 `fcop-rules.mdc`](src/fcop/rules/_data/fcop-rules.mdc)** 涓?**[瑙ｉ噴 `fcop-protocol.mdc`](src/fcop/rules/_data/fcop-protocol.mdc)**锛堥儴缃插埌 **`.cursor/rules/`**锛夈€俙spec/codeflow-core.mdc` 浠呬负**闃叉棫閾炬帴澶辨晥**鐨勫純鐢ㄥ崰浣嶏紝**鍕?*褰撴鏂囪鑼冧娇鐢ㄣ€?

**鏂瑰紡 A锛氱敤 `fcop` 搴撳垵濮嬪寲锛堟帹鑽愶級** 鈥?涓€娆″啓濂?`fcop/` 鐩綍涓?`fcop.json`锛堝簱绾﹀畾鐨勫崗浣滄牴锛夛細

```python
from fcop import Project
Project(".").init()  # 榛樿 dev-team锛涘崟浜哄彲鏀圭敤 .init_solo()
```

**鏂瑰紡 B锛氫笉璺?Python銆佸彧璁?Cursor 璇昏鍒?* 鈥?鎶婁笂鍒椾袱涓?`.mdc` 浠庢湰浠撴嫹杩涢」鐩殑 `.cursor/rules/`銆傜洰褰曡嫢灏氭湭瀛樺湪锛岃嚦灏戣鏈変笌搴撲竴鑷寸殑浜旂被妗讹細

```bash
mkdir -p fcop/{tasks,reports,issues,shared,log}
```

閰嶅ソ瑙勫垯鍚庯紝Agent 鎸夋€诲垯/瑙ｉ噴鍙煡锛氳棰嗗彂缁欒嚜宸辩殑浠诲姟銆佹寜鏂囦欢鍚嶅啓鍥炴姤鍛娿€佷笂鎶ラ棶棰樸€佷笉瓒婃潈鍔ㄤ粬浜烘枃浠躲€傛洿瀹屾暣鐨勮惤鐩樹笌鍥㈤槦妯℃澘锛岃涓嬭妭鍖呬笌 [`examples/workspace-example/`](examples/workspace-example/)銆?

## Python SDK & MCP 鏈嶅姟鍣紙鍙€夛級

鍗忚鍙函鏂囦欢閲囩撼锛?*鑻ラ渶瑕?*鍦ㄤ唬鐮侀噷璇诲啓 task/report/issue锛屾垨閫氳繃 MCP 鏆撮湶缁?IDE锛岃嚜 `0.6.0` 璧?PyPI 涓婃湁涓や釜鍖咃細

| 鍖?| 瀹夎 | 鐢ㄩ€?| 渚濊禆 |
|---|---|---|---|
| [`fcop`](https://pypi.org/project/fcop/) | `pip install fcop` | 绾?Python 搴撱€傝鍐?task / report / issue銆?*闆?MCP 渚濊禆**銆?| `pyyaml` |
| [`fcop-mcp`](https://pypi.org/project/fcop-mcp/) | `pip install fcop-mcp` | MCP 鏈嶅姟鍣ㄣ€傛妸搴撻€氳繃 stdio 鏆撮湶缁?Cursor / Claude Desktop銆?| `fcop>=1.1`銆乣fastmcp`銆乣websockets` |

**鎸囬拡琛?*锛堜竴琛屼竴浠朵簨锛屼笉缁戝畾鐗堟湰鍙凤級锛?

| 鎯冲共鍟?| 鍘昏繖閲?|
|---|---|
| 鍦?Cursor / Claude Desktop 瑁?`fcop-mcp`锛堝垎姝ャ€佸骞冲彴銆佽嚜妫€锛?| [`mcp/README.md`](mcp/README.md) |
| 涓嶆兂鑷繁鏀?JSON锛岃 agent 鍏ㄧ▼璺戝懡浠よ | [`agent-install-prompt.zh.md`](src/fcop/rules/_data/agent-install-prompt.zh.md) 路 [English](src/fcop/rules/_data/agent-install-prompt.en.md)锛堣濂戒互鍚庝篃鏄?MCP 璧勬簮 `fcop://prompt/install`锛?|
| 宸插湪鐢?0.6.x锛岃鍗囩骇锛堜袱鍖呭悓鐜涓€璧峰崌 + 鍗忚瑙勫垯鏂囦欢鍒锋柊锛?| [`docs/upgrade-fcop-mcp.md`](docs/upgrade-fcop-mcp.md) |
| 娴忚鍏ㄩ儴 45 涓伐鍏峰拰 14 涓祫婧愶紙鍒嗙被銆佷綍鏃惰皟銆佸弬鏁拌鐐癸級 | [`docs/mcp-tools.md`](docs/mcp-tools.md) |
| 鐪嬫瘡鐗堝埌搴曟敼浜嗕粈涔堛€佷负浠€涔堟敼 | [`CHANGELOG.md`](CHANGELOG.md) 涓?[`docs/releases/`](docs/releases/) |

**杩戞湡鍙戠増**锛堝畬鏁磋鏄庡湪 [`docs/releases/`](docs/releases/)锛夛細

| 鐗堟湰 | 涓€鍙ヨ瘽 |
|---|---|
| **3.2.2**锛圼CHANGELOG](CHANGELOG.md)锛?| **v3.2.2 鈥?娣卞害鍘嗗彶褰掓。 + 10 涓柊 MCP 宸ュ叿锛?5 鈫?45锛夈€?* 鏂板 `history/YYYY-MM-DD/` 鏃ユ湡鍒嗙墖闀挎湡褰掓。灞傦紱鏂板伐鍏凤細`create_task`銆乣archive_to_history`銆乣bulk_archive_to_history`銆乣list_history`銆乣get_history_stats`銆乣search_history`銆乣move_to_history`銆乣cleanup_history`銆乣export_history`銆乣import_from_history`銆傛敮鎸佹墜鍔?瀹氭椂鎶婂凡瀹屾垚浠诲姟-鎶ュ憡瀵圭Щ鍏?`history/`銆俙fcop` 涓?`fcop-mcp` 鍙屽寘 lockstep 瀵归綈鑷?3.2.2銆?|
| **3.0.2**锛圼CHANGELOG](CHANGELOG.md)锛?| **v3.0.2 鈥?鍒濆鍖栨嫇鎵戜慨澶嶃€?* 鍏抽敭 patch锛?.0.0 / 3.0.1 鐨?`Project._apply_init` 鍙垱寤轰簡 v2 鑰佹《锛岃烦杩囦簡 spec 搂1.1 寮哄埗瑕佹眰鐨?v3 `_lifecycle/{inbox,active,review,done,archive}/` 浜旀《銆?.0.2 璁?fresh init 鐩存帴钀?v3 鎷撴墤锛堝悓鏃朵笉鍐嶅垱寤鸿 superseded 鐨?v2 `tasks/` / `log/`锛夛紱`core.events.scan_workspace` 涓?`Project.role_occupancy()` 鍦?v3 椤圭洰涓嬩粠 `_lifecycle/` 璇诲彇銆傛柊澧?audit 鎵弿 `_scan_lifecycle_topology_compliance()`锛圖9锛夛細P0 = 宸插垵濮嬪寲椤圭洰鍚屾椂缂?`_lifecycle/` 鍜?v2 鍐呭锛汸1 = 涓ゅ鎷撴墤鍏卞瓨锛堝缓璁?`migrate --to-v3`锛夈€侻CP 宸ュ叿鎻忚堪锛坄init_solo` / `init_project` / `create_custom_team`锛夊悓姝ユ洿鏂般€?209 娴嬭瘯鍏ㄧ豢銆係emVer patch锛氱浉瀵?3.0.1 鏃?API 琛ㄩ潰鏀瑰姩鈥斺€攊nit 涔嬪墠鍦ㄥ仛閿欎簨銆?|
| **3.0.1**锛圼CHANGELOG](CHANGELOG.md)锛?| **v3.0.1 鈥?璺緞鏁村悎琛ヤ竵銆?* 绾枃妗?鍏冩暟鎹?patch锛屾棤浠ｇ爜閫昏緫鍙樻洿锛?.0.0 鎶?v1.0/v1.1 鍘嗗彶 spec 鑽夌绉诲埌 `spec/archived/` 鍚庯紝淇鏁ｈ惤鍦?`AGENTS.md` / `CLAUDE.md` / 鎵撳寘 Cursor rules / MCP server docstring / 涓や唤 JSON Schema `description` 涓殑澶辨晥閾炬帴锛岀粺涓€鎸囧悜 `spec/archived/fcop-runtime-protocol-v1.0.{md,zh.md}`锛堝苟鎸囬拡鍒板綋鍓?canonical `spec/fcop-3.0-spec.md`锛夈€俙fcop-mcp` 鐨?`fcop://spec` / `fcop://spec/en` docstring 鍚屾淇涓哄弽鏄?wheel 瀹為檯鎵撳寘鍐呭锛坄fcop-spec-v1.1.{lang}.md`锛夈€傚巻鍙插埗鍝侊紙TASK / REPORT / ADR / release notes / migration docs锛夋寜 ADR-0036"鍘嗗彶涓嶉噸鍐?鍘熷垯淇濈暀鍘熸枃銆?202 娴嬭瘯鍏ㄧ豢銆?|
| **3.0.0**锛圼CHANGELOG](CHANGELOG.md)锛?| **v3.0 鈥?鍗忚绾?MAJOR 路"鏂囦欢澶瑰嵆鐘舵€?绾厓銆?* FCoP 鍗忚鏈綋鐨勪竴娆″畬鏁撮噸鍐欌€斺€攃anonical 鍙屽眰锛坧er [ADR-0040](adr/ADR-0040-canonical-one-liner-two-layer-convention.md)锛夛細**Layer 1**銆屾枃浠跺嵆鍗忚锛涗綅缃畾涔夌姸鎬侊紱浜嬩欢璁板綍鍘嗗彶銆? **Layer 2** 璇箟鏈綋銆傛柊澧?`_lifecycle/{inbox,active,review,done,archive}/` 浜旀《鐩綍鎷撴墤锛?*涓?2.x 涓嶅吋瀹?*锛岄』 `fcop migrate --to-v3`锛夛紱涓夊眰瑙勫垯闆嗭紙State Layer Rule A/B/C 路 Event Layer Rule E/F/G 路 Boundary Charter锛夛紱7 鏉″厑璁歌縼绉昏〃澶栦笉鍙紙瀹炵幇 MUST 鎷掔粷锛夛紱write-then-rename 鍘熷瓙鎬фā寮忥紙浜嬩欢鍗宠縼绉伙紝杩佺Щ鍗充簨浠讹級锛汚DR-0037 Custody Layer 鍦?RFC 璇勫涓?*鏈繘 Accepted 鍗宠浣滃簾**锛坈ustody 涓嶆瀯鎴愬崗璁眰锛屼互 NOTE 褰㈠紡淇濈暀涓鸿鐢熻В閲婏級銆傛柊澧?[`spec/fcop-3.0-spec.md`](spec/fcop-3.0-spec.md) 鍗曢〉 canonical + IETF 椋庢牸 RFC 骞宠鐗?+ 涓枃骞宠鐗?+ [`docs/MIGRATION-3.0.md`](docs/MIGRATION-3.0.md) 杩佺Щ鎸囧崡銆?|
| **2.0.2**锛圼CHANGELOG](CHANGELOG.md)锛?| **v2.0.2 鈥?`fcop-mcp` 姝ｅ紡鍏ラ┗[瀹樻柟 MCP 娉ㄥ唽琛╙(https://registry.modelcontextprotocol.io/)**锛坄io.github.joinwell52-AI/fcop`锛夈€傜敱 Anthropic + GitHub + Microsoft 鑱斿悎鑳屼功鐨勫畼鏂圭洰褰曟敹褰?Claude Desktop / Cursor / PulseMCP 绛夋墍鏈?MCP 瀹㈡埛绔潎鍙竴閿彂鐜板苟閫氳繃 `uvx fcop-mcp` 瀹夎銆傚弻鍖?lockstep 鐗堟湰鍙峰榻?per ADR-0002):`fcop` 搴撲唬鐮佷笌 v2.0.0 **瀹屽叏涓€鑷?*;鏈璺ㄧ増鏈槸鎶?fcop-mcp@2.0.1 鐨?MCP-鍏冩暟鎹?patch 鍚堝苟杩涘悓鏃?release,骞惰惤鍦?鍙戠増+澶囦唤涓€鏉￠緳" SOP鈥斺€擿RULES-release-file-inventory.md`(12 绫绘竻鍗?銆乣RULES-mcp-registry-release.md`(涓夋鍗囩骇璺緞)銆佷互鍙?`joinwell52-AI/FCoP-backup` append-only 澶囦唤闀滃儚銆?|
| **2.0.0**锛圼CHANGELOG](CHANGELOG.md)锛?| **v2.0 鈥?"涓ゅ浘瀵瑰伓"鍝插灞備富鐗堟湰鍙疯法瓒娿€?* 鎵ц闈笌 v1.x 瀹屽叏涓€鑷达紙per ADR-0003 闄勫姞鎬э級锛屼富鐗堟湰鍙疯法瓒婃槸鍥犱负鍗忚灞傞娆″悓鏃舵壙璁?*涓ゅ紶鍥?*:**鎵ц鍝插鐨勪簲灞傚瀭鐩存爤**锛坴1.x 宸茬ǔ瀹氾級*涓? **FCoP Semantic Evolution Loop**锛堜竷鑺傜偣闂幆鈥斺€旀秾鐜?鈫?瑙傚療 鈫?鎻愭 鈫?璇勫 鈫?鍚堝苟 鈫?閮ㄧ讲 鈫?鍙嶅皠锛寁2.0 鏂板浐鍖栵級銆傛柊澧?Rule 4.6锛坄fcop/internal/` vs `docs/` + `essays/` 杞害瀹?+ `internal-only` 澹版槑璇硶 v1锛夈€乣Project.init(deploy_internal_template=...)` opt-in 鍙傛暟銆丳3锛堝缓璁骇锛岄潪闃诲锛夊贰鏌ヤ弗閲嶅害妗ｃ€佷互鍙?`fcop_audit` 鍐呯疆璞佸厤娓呭崟锛坄log/`/`_archive/`/`legacy-non-protocol/`锛屼慨澶?codeflow 璺ㄩ」鐩贰妫€鏆撮湶鐨勪笁涓笂娓?bug锛欼SSUE-008/009/010锛夈€侫DR-0034銆?|
| **1.6.0**锛圼CHANGELOG](CHANGELOG.md)锛?| **v1.6 鈥?Trailing-slug 鏂囦欢鍚嶆敹缂栵紙ADR-0033锛夈€?* `TASK-20260512-025-PM-to-OPS-phase-a-fix-naming.md` 杩欑被闀挎枃浠跺悕姝ｅ紡鍚堣鈥斺€旀妸 codeflow 椤圭洰 22+ 渚嬭嚜鍙戞秾鐜板啓娉曞惛鏀惰繘鏂囨硶銆俿lug 涓嶅弬涓庤矾鐢憋紝鍙槸浜虹被鍙鏍囩銆?00% 鍚戝悗鍏煎锛堟棦鏈?1057 涓崟娴?0 鍥炲綊锛夈€?|
| **1.5.0**锛圼CHANGELOG](CHANGELOG.md)锛?| **v1.5 鈥?鍗忚鎰熺煡鍚屾 + `RULE_DOC_DRIFT`銆?* 84 浠借鑹?鍥㈤槦鏂囨。鍚屾鑷?v1.4 鍗忚闈紙REVIEW envelope / `risk_level` / `fcop_audit` / `supersedes:`锛夛紱鏂板 `Project._scan_outdated_role_docs()` 鎵弿鏂规硶鍜?`RULE_DOC_DRIFT`锛圥1锛夎繚瑙勭被鍨嬨€?|
| **1.4.0**锛圼璇︾粏](docs/releases/1.4.0.md)锛?| **v1.4 鈥?Write-side 鏄惧紡缁戝畾瀹堥棬锛圥0 瀹夊叏锛? `supersedes:` 瀛楁銆?* 15 涓?write-side MCP 宸ュ叿鍦?cwd fallback 鏃剁洿鎺?`WriteRefused`锛汸rotected Path 鎷掔粷鍒楄〃锛圚OME / APPDATA / 椹卞姩鍣ㄦ牴 / Unix 绯荤粺鐩綍锛夛紱鏂板 `supersedes:` frontmatter 瀛楁锛? 绉?envelope 閫氱敤锛? `## GATE Design Pitfalls` 鑺傦紙`fcop_protocol_version 2.2.0`锛夈€?|
| **1.3.0**锛圼璇︾粏](docs/releases/1.3.0.md)锛?| **v1.3 鈥?娌荤悊鍛婅灞?+ 鍗忚宸℃煡缂栬瘧鍣ㄣ€?* GAL锛圓DR-0031锛夛細3 绫绘紓绉讳俊鍙凤紙S1/S3/S4锛夈€丗CoP-Rule-G1銆? 涓柊鍛婅宸ュ叿锛坄fcop_list_alerts`銆乣fcop_create_alert`锛夈€俙fcop_audit`锛圓DR-0032锛夛細涓夊満鏅崗璁贰鏌ョ紪璇戝櫒銆? 绉嶆壂鎻忔柟娉曘€佸甫 Execution Block 鐨?INSPECTION 鎶ュ憡銆傛€昏 35 涓?MCP 宸ュ叿銆?|
| **1.2.1**锛圼璇︾粏](docs/releases/1.2.1.md)锛?| **v1.2 鈥?Capability Governance 鏀煴銆?* `FCoPGovernanceMiddleware` 鍖呰姣忔 MCP 宸ュ叿璋冪敤锛歋kill 瑙ｆ瀽 鈫?椋庨櫓鏍囪锛圫afe / Sensitive / Critical锛夆啋 杩藉姞鍐欏叆 `fcop_events.jsonl` 瀹¤鏃ュ織銆傛柊澧?2 涓?MCP 宸ュ叿锛坄list_governance_events`銆乣get_governance_summary`锛夈€俙fcop_check()` 鏂板娌荤悊浜嬩欢鎽樿銆俙fcop` 涓?`fcop-mcp` 鍚屾瀵归綈鑷?`1.2.1`锛堥攣姝ュ彂鐗堬級銆侫DR-0030-bis銆?|
| **1.1.0**锛圼CHANGELOG](CHANGELOG.md)锛?| **v1.1 鈥?Agent.layer 娌荤悊鍚堢害 + Task.risk_level + Review.needs_human + HumanApproval + Skill.tools[] 椋庨櫓鍏冩暟鎹€?* 5 鏉℃柊 ADR锛?023鈥?027锛夛紝4 涓柊 MCP 宸ュ叿锛坄write_review`銆乣list_reviews`銆乣read_review`銆乣mark_human_approved`锛夛紝`write_task` 鏂板 `risk_level` 鍙傛暟锛屾柊澧?`skill.schema.json`銆傚畬鍏ㄥ悜鍚庡吋瀹广€?|
| **1.0.1** | spec 鏂囦欢鎵撳寘杩?wheel锛坄get_spec()`锛夛紱`fcop://spec` MCP 璧勬簮锛泈orkspace 璺緞杩佺Щ `docs/agents/` 鈫?`fcop/`锛汣I 鍏ㄧ豢銆?|
| **1.0.0** | 涓冨ぇ鏍稿績姒傚康鍥哄寲锛欰gent銆丒ncoding銆両PC銆丒vent銆丗ailure銆丅oundary銆丄udit銆? 涓?JSON Schema銆傝[鍙戝竷璇存槑](docs/releases/1.0.0.md)銆?|
| **0.7.2**锛圼璇︾粏](docs/releases/0.7.2.md)锛?| 鍏冩暟鎹?patch锛氫慨 `fcop-rules.mdc` frontmatter 閿欑増鏈彿銆傛棤鍗忚鍙樺寲銆佹棤 API 鍙樺寲銆?|

> **灏忓績锛歅yPI 涓婃湁涓€涓窡杩欓噷鏃犲叧鐨?`fcop` 鍚屽悕鍖呫€?* 鏈粨涓や釜鍖呴兘浠?*鏈粨鍙?*銆傚鏋?`pip install fcop` 涔嬪悗 `from fcop import Project, Issue` 浠嶅け璐ワ紝澶氬崐鏄綘瑁呴敊浜?distribution銆佹垨鏈満鏌愪釜鍙紪杈戝畨瑁呯殑宸ョ▼鎶?`fcop` 鍚嶅瓧鎶㈣蛋浜嗐€備慨娉曪細骞插噣 venv + 涓€骞舵寜 PyPI 閲嶈涓や釜鍖呫€傞獙璇佸懡浠ゅ湪 [`mcp/README.md`](mcp/README.md)銆?

**搴?* 鈥斺€?浠庝换浣?Python 鑴氭湰鎴?agent 閲岀洿鎺ヨ皟锛?

```python
from fcop import Project

proj = Project(".")                              # 椤圭洰鏍癸紱鏈?init 鏃舵棤 fcop.json
proj.init()                                      # 寤?tasks|reports|issues|shared|log/ 涓?fcop.json
task = proj.write_task(sender="PM", recipient="DEV", priority="P1",
                       subject="鍔犻壌鏉冧腑闂翠欢", body="...",
                       risk_level="high")        # v1.1锛氳Е鍙?needs_human review gate
print(proj.list_tasks(recipient="DEV"))
```

**MCP 鏈嶅姟鍣?* 鈥斺€?鍐欒繘 Cursor 鐨?`mcp.json` 鎴?Claude Desktop 鐨?`claude_desktop_config.json`锛?

```json
{
  "mcpServers": {
    "fcop": {
      "command": "uvx",
      "args": ["fcop-mcp"]
    }
  }
}
```

**涓嶆兂鑷繁鏀?JSON锛?* 璁?agent 鏉ャ€傚紑涓€涓兘璺戝懡浠ょ殑鏂颁細璇濓紝鎶婂畼鏂瑰畨瑁呮彁绀鸿瘝
锛圼`agent-install-prompt.zh.md`](src/fcop/rules/_data/agent-install-prompt.zh.md)
路 [English](src/fcop/rules/_data/agent-install-prompt.en.md)锛夋暣娈佃创杩囧幓鈥斺€?
agent 浼氳瘑鍒郴缁熴€佽 `uv`銆佹敼 `mcp.json`锛?*淇濈暀**宸叉湁 server锛夈€佹彁閱掗噸鍚€?
瑁呭ソ浠ュ悗杩欐鎻愮ず璇嶅湪 MCP 璧勬簮 `fcop://prompt/install` 涔熻兘鐩存帴璇诲埌銆傛彁绀?
璇嶉噷**鏄庝护绂佹** agent 瑁呭畬椤烘墜 `init_project`鈥斺€斿垵濮嬪寲鏄?ADMIN 鐨勪笁閫変竴
锛坰olo / 棰勮鍥㈤槦 / 鑷畾涔夛級锛屼笉鏄?agent 鐨勯粯璁ゅ€笺€?

绋冲畾鎬ф壙璇猴細**鏁翠釜 `0.6.x` 灏忕増鏈懆鏈熷唴鍙姞涓嶆敼**锛岃瑙?[`adr/ADR-0003-stability-charter.md`](adr/ADR-0003-stability-charter.md)銆?

> **浠?0.7.x 鍗囩骇鍒?v1.0锛?* workspace 榛樿鐩綍浠?`docs/agents/` 杩佸埌椤跺眰 `fcop/`锛坧er [ADR-0022](adr/ADR-0022-workspace-directory-convention.md)锛夈€備竴閿?git-aware 杩佺Щ锛歚fcop migrate-workspace --apply`锛涗笉鎯冲姩鐩樹紶 `Project(workspace_dir="docs/agents")` 鍗冲彲姘镐箙閿佸畾鑰?layout銆傚畬鏁?walkthrough锛堝惈 4 涓柊鎶借薄 REVIEW / Failure / Boundary / Event + JSON Schema 闆嗘垚锛夎 [`docs/MIGRATION-1.0.md`](docs/MIGRATION-1.0.md)銆?
>
> **浠?0.5.x 鍗囩骇锛?* MCP 鏈嶅姟鍣ㄥ凡浠?`fcop` 鍖呮惉鍒?`fcop-mcp`鈥斺€旀妸 `mcp.json` 閲岀殑鍛戒护鏀规垚 `uvx fcop-mcp`銆傚畬鏁磋縼绉绘寚寮曡 [`docs/MIGRATION-0.6.md`](docs/MIGRATION-0.6.md)锛屾湰娆″彂鐗堟。妗堣 [`docs/releases/0.6.0.md`](docs/releases/0.6.0.md)銆?

## 濡備綍闃呰 FCoP 鏂囨。

## 濡備綍闃呰 FCoP 鏂囨。

| 浣犵殑鐩爣 | 浠庤繖閲屽紑濮?|
|---|---|
| **FCoP 鏂版墜** 鈥?45 鍒嗛挓涓婃墜瀹炴垬 | [`docs/getting-started.md`](docs/getting-started.md) |
| **浠?0.7.x 鍗囩骇** 鈥?workspace 杩佺Щ + 4 涓柊姒傚康 | [`docs/MIGRATION-1.0.md`](docs/MIGRATION-1.0.md) |
| **浠?1.0/1.1 鍗囩骇鍒?1.2** 鈥?Capability Governance + 閿佹鍙戠増 | [`docs/MIGRATION-1.1.md`](docs/MIGRATION-1.1.md) 路 [CHANGELOG](CHANGELOG.md) |
| **鐞嗚В鍗忚濂戠害** 鈥?鍚堣瀹炵幇 MUST 鍋氫粈涔?| [`spec/fcop-3.0-spec.zh.md`](spec/fcop-3.0-spec.zh.md) 鈥?鍗曢〉姝ｅ紡瑙勮寖 v3.0锛堜腑鏂囷級銆倂1.0/v1.1 鏃╂湡 spec 鑽夌鍦?`spec/` 涓繚鐣欎綔涓哄巻鍙插弬鑰冦€?|
| **v1.2 Capability Governance** 鈥?FCoPGovernanceMiddleware銆侀闄╂爣璁般€佸璁℃棩蹇?| [CHANGELOG](CHANGELOG.md) 路 ADR-0030-bis |
| **v1.1 鏂板瓧娈?* 鈥?risk_level銆乶eeds_human銆乭uman_approval銆乻kill tools | [CHANGELOG](CHANGELOG.md) 路 ADR-0023..0027 |
| **鐞嗚В鍐崇瓥鑳屽悗鐨勫師鍥?* 鈥?姣忎釜璁捐鐨勮€冮噺 | [`adr/`](adr/) 鈥?浠?[ADR-0029](adr/ADR-0029-fcop-behavior-governance-charter.md) 寮€濮?|
| **鍏ㄩ儴 45 涓?MCP 宸ュ叿涓?14 涓祫婧?* | [`docs/mcp-tools.md`](docs/mcp-tools.md) |
| **鍙戝竷璇存槑** 鈥?瀹屾暣鍙樻洿鏃ュ織 | [`CHANGELOG.md`](CHANGELOG.md) |
| **瀹屾暣鏂囨。鍦板浘** 鈥?姣忎釜鏂囦欢鐨勮鑹?| [`adr/README.md`](adr/README.md)锛圓DR 绱㈠紩锛? [`spec/fcop-3.0-spec.zh.md`](spec/fcop-3.0-spec.zh.md) 搂11锛堝紩鐢ㄦ潗鏂欙級|

---

## 璁捐鍘熷垯

1. **鏂囦欢鍚嶆槸鍞竴鐪熺悊銆?*鐩綍 + 鏂囦欢鍚嶅喅瀹氱姸鎬侊紝frontmatter 鍙槸鍐椾綑鍏冩暟鎹€?
2. **鍘熷瓙鎬ф潵鑷?`rename()`**銆傛病鏈夊埆鐨勨€斺€斾笉闇€瑕侀攣锛屼笉闇€瑕佷簨鍔°€?
3. **浜烘満鍚屾瀯銆?*`cat` 鑳借鐨勫氨鏄?Agent 鑳借В鏋愮殑锛屾病鏈夎皟璇曟ā寮忋€佹病鏈夌鐞嗗悗鍙般€?
4. **韬唤鍐冲畾璺緞銆?*鏂囦欢鍚嶉噷鐨勮鑹叉爣璇嗘湰韬氨鏄潈闄愭ā鍨嬧€斺€旇韩浠戒笉鍖归厤锛孉gent 杩炴枃浠堕兘鍔ㄤ笉浜嗐€?
5. **闆跺熀纭€璁炬柦銆?*鍙鏈夋枃浠剁郴缁熷氨鏈?FCoP銆傜瑪璁版湰鑳借窇锛岄泦缇よ兘璺戯紝璺ㄦ満閫氳繃 `rsync` 灏辫兘璺戙€?

## 鍙傝€冨疄鐜?

涓ゅ瀹樻柟鍙傝€冨疄鐜帮紝鍧囦负 MIT 璁稿彲锛?

1. **`fcop` / `fcop-mcp`** 鈥斺€?鍗忚鐨?Python 搴?+ MCP 鏈嶅姟鍣ㄣ€傛簮鐮佸湪鏈粨搴?[`src/fcop/`](src/fcop/) 鍜?[`mcp/src/fcop_mcp/`](mcp/src/fcop_mcp/)锛岄€氳繃 PyPI 鍒嗗彂锛堣涓婁竴鑺傦級銆?
2. **鍘嗗彶 URL 鍗犱綅**锛歚spec/codeflow-core.mdc` 浠呴槻鏃ч摼鎺ュけ鏁堬紝**鏃犳鏂?*锛?*鍞竴鏉冨▉**浠嶆槸 `src/fcop/rules/_data/fcop-rules.mdc` + `fcop-protocol.mdc`锛堟枃浠跺悕鍚巻鍙插瓧鏍疯€屽凡锛夈€?

## 鐘舵€佷笌鐗堟湰

- **褰撳墠鍙戝竷**锛歚v3.2.2`锛?026-05-22锛夆€斺€?*鍒濆鍖栨嫇鎵戜慨澶嶃€?* 鍏抽敭 patch锛?.0.0 / 3.0.1 鐨?`Project._apply_init` 鍙垱寤轰簡 v2 鑰佹《锛岃烦杩囦簡 spec 搂1.1 寮哄埗瑕佹眰鐨?v3 `_lifecycle/{inbox,active,review,done,archive}/` 浜旀《鈥斺€旀墍鏈夊湪閭ｄ袱鐗堜笂 fresh init 鐨勯」鐩兘鏄?*鐢熻€屼笉鍚堣**鐨勩€?.0.2 璁?fresh init 鐩存帴钀?v3 鎷撴墤锛堝悓鏃朵笉鍐嶅垱寤鸿 superseded 鐨?v2 `tasks/` / `log/`锛夛紱`core.events.scan_workspace` 涓?`Project.role_occupancy()` 鍦?v3 椤圭洰涓嬩粠 `_lifecycle/` 璇诲彇銆傛柊澧?audit 鎵弿 `_scan_lifecycle_topology_compliance()`锛圖9锛夛細P0 = 宸插垵濮嬪寲椤圭洰鍚屾椂缂?`_lifecycle/` 鍜?v2 鍐呭锛汸1 = 涓ゅ鎷撴墤鍏卞瓨锛堝缓璁?`migrate --to-v3`锛夈€侻CP 宸ュ叿鎻忚堪锛坄init_solo` / `init_project` / `create_custom_team`锛夊悓姝ユ洿鏂般€?209 娴嬭瘯鍏ㄧ豢銆係emVer patch锛氭棤 API 琛ㄩ潰鏀瑰姩鈥斺€攊nit 涔嬪墠鍦ㄥ仛閿欎簨銆傚墠缃?**v3.0.1**锛?026-05-21锛夆€斺€?璺緞鏁村悎琛ヤ竵锛堢函鏂囨。锛夈€傚墠缃?**v3.0.0**锛?026-05-21锛夆€斺€?**鍗忚绾?MAJOR 路"鏂囦欢澶瑰嵆鐘舵€?绾厓**锛欶CoP 鍗忚鏈綋鐨勪竴娆″畬鏁撮噸鍐欌€斺€攃anonical 鍙屽眰锛坧er [ADR-0040](adr/ADR-0040-canonical-one-liner-two-layer-convention.md)锛夈€屾枃浠跺嵆鍗忚锛涗綅缃畾涔夌姸鎬侊紱浜嬩欢璁板綍鍘嗗彶銆? 璇箟鏈綋锛涙柊澧?`_lifecycle/{inbox,active,review,done,archive}/` 浜旀《鐩綍鎷撴墤锛?*涓?2.x 涓嶅吋瀹?*锛岄』 `fcop migrate --to-v3`锛夛紱涓夊眰瑙勫垯闆嗭紙State / Event / Boundary Charter锛? 7 鏉″厑璁歌縼绉昏〃澶栦笉鍙?+ write-then-rename 鍘熷瓙鎬э紱ADR-0037 Custody Layer 鍦?RFC 璇勫涓?*鏈繘 Accepted 鍗宠浣滃簾**銆傝瑙?[`spec/fcop-3.0-spec.md`](spec/fcop-3.0-spec.md) 涓?[`docs/MIGRATION-3.0.md`](docs/MIGRATION-3.0.md)銆傛棭鏈熷彂甯冿細v2.0.2锛坒cop-mcp 鍏ラ┗瀹樻柟 MCP 娉ㄥ唽琛級銆乿2.0.0锛堜袱鍥惧鍋跺摬瀛︿富鐗堟湰鍙疯法瓒?+ Rule 4.6 `fcop/internal/`锛夈€乿1.6锛坱railing-slug 鏂囦欢鍚嶆敹缂栵紝ADR-0033锛夈€乿1.5锛?4 浠藉崗璁劅鐭ュ悓姝ワ級銆乿1.4锛坵rite-side 瀹堥棬 + `supersedes:` 瀛楁锛夈€乿1.3锛圙AL + `fcop_audit()` 宸℃煡缂栬瘧鍣級銆乿1.2.1锛圕apability Governance 鏀煴锛夈€乿1.1锛圓gent.layer + Task.risk_level + needs_human锛夈€乿1.0锛堜竷澶ф牳蹇冩蹇?spec freeze锛夈€傝瑙?[CHANGELOG](CHANGELOG.md)銆?
- **瑙勮寖鎬ф枃浠?*锛歔`spec/fcop-3.0-spec.zh.md`](spec/fcop-3.0-spec.zh.md)锛堜腑鏂?v3.0锛壜?[`spec/fcop-3.0-spec.md`](spec/fcop-3.0-spec.md)锛堣嫳鏂囨潈濞?v3.0锛壜?v1.0/v1.1 鏃╂湡 spec 鑽夌鍦?`spec/` 涓繚鐣欎綔涓哄巻鍙插弬鑰?路 鏈哄櫒鍙濂戠害瑙?[`spec/schemas/`](spec/schemas/)锛? 涓?Schema锛?
- **鏈粨鍐?Agent 瑙勫垯锛坄.mdc`锛?*锛歔`src/fcop/rules/_data/fcop-rules.mdc`](src/fcop/rules/_data/fcop-rules.mdc) + [`fcop-protocol.mdc`](src/fcop/rules/_data/fcop-protocol.mdc)锛坄spec/codeflow-core.mdc` 浠呬负寮冪敤鍗犱綅锛?
- **鍙樻洿璁板綍**锛歔`CHANGELOG.md`](CHANGELOG.md)
- **鐮旂┒蹇収**锛歔`research-snapshot-2026-04-29`](https://github.com/joinwell52-AI/FCoP/releases/tag/research-snapshot-2026-04-29) 宸茬粡褰掓。鍒?Zenodo 骞跺垎閰?DOI锛堣瑙佷笅鏂?*濡備綍寮曠敤*锛夈€?

## 濡備綍寮曠敤

濡傛灉 FCoP 鐨勫崗璁€佺幇鍦烘姤鍛?essays銆佹暀绋嬨€佹垨鍙傝€冨疄鐜板浣犵殑鐮旂┒銆佽蒋浠躲€佸啓浣滄湁甯姪锛岃寮曠敤 [Zenodo 鐮旂┒蹇収](https://doi.org/10.5281/zenodo.19886036)锛?

- **DOI**锛歔`10.5281/zenodo.19886036`](https://doi.org/10.5281/zenodo.19886036)
- **蹇収 tag**锛歔`research-snapshot-2026-04-29`](https://github.com/joinwell52-AI/FCoP/releases/tag/research-snapshot-2026-04-29)锛坈ommit `7f59395`锛?
- **鏈哄櫒鍙鍏冩暟鎹?*锛歔`CITATION.cff`](CITATION.cff)锛圙itHub 浼氫粠杩欎釜鏂囦欢鑷姩娓叉煋涓€涓?*Cite this repository* 鎸夐挳鏀惧湪鍙虫爮锛?

```bibtex
@misc{fcop2026snapshot,
  author       = {Zhu, Wei},
  title        = {{FCoP}: A Filename-as-Protocol coordination layer for multi-agent {AI} development (Research Snapshot, April 2026)},
  month        = apr,
  year         = 2026,
  publisher    = {Zenodo},
  version      = {research-snapshot-2026-04-29},
  doi          = {10.5281/zenodo.19886036},
  url          = {https://doi.org/10.5281/zenodo.19886036}
}
```

濡傛灉寮曠敤鍗曠瘒 essay 鎴栨暀绋嬶紝DOI 浠嶆槸鍚屼竴涓€斺€斿湪寮曠敤鑴氭敞閲岄檮涓?essay 鐨勬枃浠跺悕锛堝 `essays/what-agents-say-about-fcop.md`锛夊拰 snapshot 鐗堟湰鍙峰嵆鍙畾浣嶅埌鍏蜂綋鍐呭銆?

## 濡備綍璐＄尞

鏈粨搴撳埢鎰忎繚鎸?*灏忚€岀ǔ**銆傚崗璁紨杩涚殑渚濇嵁鏄?鐪熷疄鍦烘櫙閲岀殑鎶ュ憡"锛屼笉鏄?濮斿憳浼氭姇绁?銆傛渶鏈変环鍊肩殑璐＄尞鏄細

1. **鐜板満鎶ュ憡銆?*鎶?FCoP 鎷夊埌浣犺嚜宸辩殑 Agent 鍥㈤槦閲岃窇涓€娈碉紝鎶?鍝噷鍧忎簡"銆?Agent 鑷繁鍙戞槑浜嗕粈涔?銆?娑岀幇鍑哄摢浜涘懡鍚嶇害瀹?寮€涓?Issue銆?
2. **绉绘涓?SDK銆?*Python / TypeScript / Go 鐨勮杽灏佽锛岃礋璐ｈВ鏋愭枃浠跺悕鍜岃窇 `rename()` 鐘舵€佹満銆?
3. **缂栬緫鍣ㄤ笌 MCP 闆嗘垚銆?*`.fcop` 鏂囦欢鐨勮娉曢珮浜€佹妸杩欏鏂囦欢澶?expose 缁欏叾浠?Agent 杩愯鏃剁殑 MCP 妗ャ€?

瀵硅鑼冩湰韬殑 PR锛岃閾炬帴鍒板畠瑕佽В鍐崇殑鍏蜂綋闂銆?

## License

MIT 鈥?璇﹁ [LICENSE](LICENSE)銆?

## 鑷磋阿

FCoP 鏄湪 **Cursor 绛夌幆澧?*閲屼笌澶?Agent 瀹炴垬鍗忎綔鏃堕檰缁秾鐜扮殑銆傝鑼冮噷涓嶅皯绾﹀畾**鏈€鍒濇槸 Agent 浠嚜宸卞啓鍑烘潵鐨?*锛屾垜浠彧鏄妸瀹冧滑鏁寸悊鎴愬唽銆傝鎯呰 [鐜板満鎶ュ憡](essays/when-ai-organizes-its-own-work.md)銆?
