# Changelog

<!--next-version-placeholder-->

## v3.1.4 (2023-08-16)

### Fix

* Update autobisect to fix LD_LIBRARY_PATH issue ([`2b154a4`](https://github.com/MozillaSecurity/bugmon/commit/2b154a445437e99f129c288b639a76ab2be6ac60))

## v3.1.3 (2023-08-15)

### Fix

* Update autobisect to set LD_LIBRARY_PATH to build dir for js shell ([`630e95e`](https://github.com/MozillaSecurity/bugmon/commit/630e95e512de8e38fcd999e4faab61381033f8b7))
* Allow non-fuzzing builds in config iterator ([`21cff9a`](https://github.com/MozillaSecurity/bugmon/commit/21cff9a76bbf1f6f9879466950c88188b05aeb28))
* Don't check existing bug flags when generating products ([`a56aad9`](https://github.com/MozillaSecurity/bugmon/commit/a56aad92b45561209c7cc695a807ffcb6ad68086))

## v3.1.2 (2023-07-14)

### Fix

* Expand list of build configurations to avoid ([`de44324`](https://github.com/MozillaSecurity/bugmon/commit/de44324b95c8c2ac457441cfbc6798fee87638cd))
* Catch failed attempts at fetching builds ([`c29532d`](https://github.com/MozillaSecurity/bugmon/commit/c29532de82d7279b025cebefea7879273e2a6e57))

## v3.1.1 (2023-06-12)

### Fix

* Avoid non-fuzzing debug builds now that crashreporter-symbols.zip is no longer indexed ([`880baff`](https://github.com/MozillaSecurity/bugmon/commit/880baff111421f2e2c5f6c04d80a47ab84edcb37))

## v3.1.0 (2023-06-12)

### Feature

* Add asan to the build flag iterator ([`3a44d5f`](https://github.com/MozillaSecurity/bugmon/commit/3a44d5f806d68c13ceb691b2c9b05c33f101c962))

### Fix

* Avoid opt builds now that crashreporter-symbols.zip is no longer indexed ([`90a8889`](https://github.com/MozillaSecurity/bugmon/commit/90a88895585a44328a0f19bf7e9327a857df0d24))

## v3.0.2 (2023-06-08)

### Fix

* Autobisect update includes fix for recent taskcluster build changes ([`13f7524`](https://github.com/MozillaSecurity/bugmon/commit/13f752497325e6608df59963d358c539684280d8))

## v3.0.1 (2023-05-03)
### Fix
* Update autobisect to 7.0.1 ([`3ab270a`](https://github.com/MozillaSecurity/bugmon/commit/3ab270a22c362a4bc8fd2497c4898ef633df4994))

## v3.0.0 (2023-04-25)
### Feature
* Update autobisect to v7.0.0 ([`4852dba`](https://github.com/MozillaSecurity/bugmon/commit/4852dba01d4dc8c5a293ff05a3a5b3ead47264f5))

### Breaking
* drop support for python 3.7 ([`87b5d98`](https://github.com/MozillaSecurity/bugmon/commit/87b5d98d93c012e72adbe3092cb42760c9a5f02a))

## v2.4.0 (2023-04-14)
### Feature
* Add pernosco-failed status command ([`b7ae968`](https://github.com/MozillaSecurity/bugmon/commit/b7ae9686c657ef01576cf40903d4f3794cd5f8f9))

## v2.3.2 (2023-03-01)
### Fix
* Report pernosco-submit error on failure ([`3dbd79d`](https://github.com/MozillaSecurity/bugmon/commit/3dbd79d0137cf73fd0cf8a52e75048f4706293c5))

## v2.3.1 (2023-03-01)
### Fix
* Add punctuation to report messages ([`675dbe5`](https://github.com/MozillaSecurity/bugmon/commit/675dbe5e20300576bf642a85bf89dc8d2a62cc53))

## v2.3.0 (2023-02-23)
### Feature
* Update pernosco related keywords if trace successful ([`e357be2`](https://github.com/MozillaSecurity/bugmon/commit/e357be2c5b2ed495117608c8017327829335a577))

## v2.2.0 (2023-02-21)
### Feature
* Replace confirm/verify commands with analyze ([`8683418`](https://github.com/MozillaSecurity/bugmon/commit/86834183067a3064f4f44e50bd2704f739f619ef))

### Fix
* Check that command exists before adding or removing it ([`17ee883`](https://github.com/MozillaSecurity/bugmon/commit/17ee883b64f5a9201f443ecb5ec809b73a396463))

## v2.1.4 (2022-12-06)
### Fix
* Report success on pernosco before upload ([`492378f`](https://github.com/MozillaSecurity/bugmon/commit/492378f8471d8ee2a7dfb5ad69736665db0e30f8))

## v2.1.3 (2022-12-01)
### Fix
* Update fuzzfetch ([`4d533ae`](https://github.com/MozillaSecurity/bugmon/commit/4d533ae6b92cc4ac389118e15e3c74f2c5e55c4d))

## v2.1.2 (2022-12-01)
### Fix
* Log pernosco-submit error message ([`784be5c`](https://github.com/MozillaSecurity/bugmon/commit/784be5c38b15826f71f0db0d5577f91357bc913d))

## v2.1.1 (2022-11-30)
### Fix
* Minor change in bug comment ([`3acfef8`](https://github.com/MozillaSecurity/bugmon/commit/3acfef8b96e7029401287725d0ac569d288f71d9))

## v2.1.0 (2022-11-07)
### Feature
* Relaunch browser after every attempt ([`83f1d19`](https://github.com/MozillaSecurity/bugmon/commit/83f1d1982e1e3a57141f123d51de487e505ee048))

## v2.0.4 (2022-10-28)
### Fix
* Use default timeout for browser evaluator ([`b131550`](https://github.com/MozillaSecurity/bugmon/commit/b13155032a436ff513d893755823c533b4daad0e))
* Set grizzly time-limit instead of timeout for pernosco sessions ([`1344f10`](https://github.com/MozillaSecurity/bugmon/commit/1344f100e6d23b2343f791daa2efdd3a9e3ca0e8))
* Minor changes to logging and comment output ([`d272d3c`](https://github.com/MozillaSecurity/bugmon/commit/d272d3c0e90dd574152bf64e4f64bc0d793ffde9))
* Require pernosco creds in submit_pernosco ([`2949a4c`](https://github.com/MozillaSecurity/bugmon/commit/2949a4cc7e07366236ee70ef10ebe7f31e62f35d))
* Remove pernosco creds from environment ([`78c5898`](https://github.com/MozillaSecurity/bugmon/commit/78c5898ed660cfb489a146dfc3a1f22f433e22ea))

## v2.0.3 (2022-10-20)
### Fix
* Post to bug that pernosco session has been recorded ([`bf030c9`](https://github.com/MozillaSecurity/bugmon/commit/bf030c94d189529a9de1f36916c6f6261bfac9dd))

## v2.0.2 (2022-10-20)
### Fix
* Update path to pernoscoshared lib ([`8ac091b`](https://github.com/MozillaSecurity/bugmon/commit/8ac091bd464e760b770af4ef073399316f9beb8b))

## v2.0.1 (2022-10-20)
### Fix
* Update autobisect to ensure log path is set ([`4722d0e`](https://github.com/MozillaSecurity/bugmon/commit/4722d0e26324ad23f52be5f1f9e85576761a53df))

## v2.0.0 (2022-10-20)
### Feature
* Export BugmonException ([`e30804a`](https://github.com/MozillaSecurity/bugmon/commit/e30804a2bb4d51c0b75e51a3a241c39ad2c0c2b7))
* Add support for record pernosco sessions ([`778599f`](https://github.com/MozillaSecurity/bugmon/commit/778599fe6bf4228f3376fd0815dd0993ffef3e44))

### Fix
* Conditionally import typing_extensions for py37 ([`886f9a3`](https://github.com/MozillaSecurity/bugmon/commit/886f9a33a107003619dcbcb8f624c352e1ac3827))
* Use __name__ when declaring logger ([`145f4e5`](https://github.com/MozillaSecurity/bugmon/commit/145f4e5a0312906c3a76603efc555e22f771cb4a))

### Breaking
* This commit makes numerous changes to the BugMonitor API  ([`778599f`](https://github.com/MozillaSecurity/bugmon/commit/778599fe6bf4228f3376fd0815dd0993ffef3e44))

### Documentation
* Minor pydoc updates ([`36f9c2e`](https://github.com/MozillaSecurity/bugmon/commit/36f9c2e9196554b96d1295d38cb905ccb3b7cee0))

## v1.3.2 (2022-09-27)
### Fix
* Update autobisect to ensure relaunch is set to 1 ([`695b80f`](https://github.com/MozillaSecurity/bugmon/commit/695b80f7863664b3fc68284a233f1024979180e2))

## v1.3.1 (2022-07-07)
### Fix
* Remove verify from commands after verification ([`e22d8a5`](https://github.com/MozillaSecurity/bugmon/commit/e22d8a59ba5ef2b5aa5f88cdbfa992436dd7cc66))

## v1.3.0 (2022-06-03)
### Feature
* Add needinfo flag if bug fixed prematurely ([`b16fde7`](https://github.com/MozillaSecurity/bugmon/commit/b16fde72b2518a05d62ce4c2e91389dd7896d6e1))
* Add method for setting the needinfo flag ([`b097be1`](https://github.com/MozillaSecurity/bugmon/commit/b097be18d8237c6f0dd21a8fcff4db9147797896))
* Add property for retrieving the assignee or creator ([`b81bd1b`](https://github.com/MozillaSecurity/bugmon/commit/b81bd1bd77fedeebcf38621d2ffcc0f8a89f461c))

### Fix
* Add typing_extensions import for py37 ([`81f6a30`](https://github.com/MozillaSecurity/bugmon/commit/81f6a30409e785fe7d10f76afe533dabd04a3a44))
* Minor reporter formatting changes ([`d3a9b2d`](https://github.com/MozillaSecurity/bugmon/commit/d3a9b2d6fa7bb9b4975b2ba97e4f0ee993a0ffae))

### Documentation
* Add comment ([`cc8128e`](https://github.com/MozillaSecurity/bugmon/commit/cc8128e20ba77fa3c421529cf3a1fb35c557b7d4))
* Fix indent ([`604c0ed`](https://github.com/MozillaSecurity/bugmon/commit/604c0ed33baa7d8542ad92dfbcc4f4538ff32a5e))

## v1.2.4 (2022-06-01)
### Fix
* Exclude nyx builds ([`8f17265`](https://github.com/MozillaSecurity/bugmon/commit/8f1726591948a100cad50f5a4866e10577803556))
* Update autobisect to fix fuzzfetch errors ([`596646b`](https://github.com/MozillaSecurity/bugmon/commit/596646b3dc052e42d3d3a72029e61d2ea7bd00e3))

## v1.2.3 (2022-04-29)
### Fix
* Exit early if no fix commit found ([`f755a43`](https://github.com/MozillaSecurity/bugmon/commit/f755a43dc07b595e8beb10e5c329bdb4f2f8c46a))

## v1.2.2 (2022-04-22)
### Fix
* Only set status to verified if not new ([`b5153ab`](https://github.com/MozillaSecurity/bugmon/commit/b5153ab9baab4d3c16f128f04c7b8ae5db1aba37))

## v1.2.1 (2022-04-04)
### Fix
* Update autobisect to v5.0.0 ([`a8bf24c`](https://github.com/MozillaSecurity/bugmon/commit/a8bf24c13e00b281ee8e3439e0534ffbe687de08))
* Update autobisect to 3.1.9 ([`200c7d5`](https://github.com/MozillaSecurity/bugmon/commit/200c7d5c754930d1ead26441f576d84da3a026b3))

## v1.2.0 (2022-03-02)
### Feature
* Add regression keyword if bisection succeeds ([`963ca70`](https://github.com/MozillaSecurity/bugmon/commit/963ca7026c491e72f067152461277e6f32236ffe))

### Fix
* Update lockfile to correct breakage in grizzly ([`9fc9dfa`](https://github.com/MozillaSecurity/bugmon/commit/9fc9dfa44ae6876ec0e958bb080b36b39b897d46))
* Remove unused mypy comment ([`378fa22`](https://github.com/MozillaSecurity/bugmon/commit/378fa22caddd0f2f3f79bacb4de3abf7c17992a6))
* Catch attempts to initialize bisector with an invalid range ([`e1e1b06`](https://github.com/MozillaSecurity/bugmon/commit/e1e1b069e03321a0c542b79689d02abc2cf3b649))
* Expand failed verification message ([`8b23c11`](https://github.com/MozillaSecurity/bugmon/commit/8b23c1123b4d91359b48b8aea04cd8e294768984))
* Identify testcases recursively ([`81979a9`](https://github.com/MozillaSecurity/bugmon/commit/81979a98a3e09eb46365d22052139775b665ac1e))
* Exclude prefs from possible entry points ([`4ff9789`](https://github.com/MozillaSecurity/bugmon/commit/4ff978916ef1ccaf5f81695e20d739d4f09f3e5b))
* Fix name for accessibility component ([`89ab663`](https://github.com/MozillaSecurity/bugmon/commit/89ab663a2cfcf3d7dd198b33766fc7c8a8f6fa72))
* Set explicit type hint ([`1fab91a`](https://github.com/MozillaSecurity/bugmon/commit/1fab91a49ae451d58550b8d208a716dc6eac79da))
* Add free-form params attr for reporting configuration ([`299faf1`](https://github.com/MozillaSecurity/bugmon/commit/299faf1f477259a3a2b97f39822807c2e8d4ed82))
* Update autobisect to ignore unhandleable ooms ([`ff39c29`](https://github.com/MozillaSecurity/bugmon/commit/ff39c29b5e73dfd124ffdd77bd7730c26532e066))

### Documentation
* Fix report pydoc params ([`b7bc1f4`](https://github.com/MozillaSecurity/bugmon/commit/b7bc1f4970f307ef5f2de264db9c0049454c4bdf))

## v1.1.3 (2021-09-01)
### Fix
* Filter out directories during testcase iteration ([`f9f6270`](https://github.com/MozillaSecurity/bugmon/commit/f9f62708b43c21930e8d058e50e4d7b994ba3c87))
* Simplify pref detection ([`0a12517`](https://github.com/MozillaSecurity/bugmon/commit/0a1251789f3eb411b6801fafe9ef27d07f6d7a5d))
* Catch Fetcher errors when artifact doesn't exist ([`d010ab8`](https://github.com/MozillaSecurity/bugmon/commit/d010ab839a0fc2af5f8b2a425161b91fb0122e67))
* Only close bug if we actually tested the original build ([`9ef08f2`](https://github.com/MozillaSecurity/bugmon/commit/9ef08f2014a56d2fd36f4c546b50a5e8a2653d9e))
* Improve logging when bug repros on tip but not initial ([`9261167`](https://github.com/MozillaSecurity/bugmon/commit/92611676d4693c51707489c1254722ce58d07d15))

## v1.1.2 (2021-08-17)
### Fix
* Don't yield the same build flags more than once ([`fdbf79f`](https://github.com/MozillaSecurity/bugmon/commit/fdbf79f83b1f1519b74d6dbea0fc36a021e3eed8))

## v1.1.1 (2021-08-06)
### Fix
* Move unnecessary deps to dev-dependencies ([`ced1ad8`](https://github.com/MozillaSecurity/bugmon/commit/ced1ad85250c86768001378bec91e001e19d5924))

## v1.1.0 (2021-08-06)
### Feature
* Add harness iterator for BrowserEvaluator ([#23](https://github.com/MozillaSecurity/bugmon/issues/23)) ([`5d127fb`](https://github.com/MozillaSecurity/bugmon/commit/5d127fbfc0e7b4171dd4f490c6420f5b296b0c7d))

### Fix
* Only force confirmation if no other action applies ([`751f917`](https://github.com/MozillaSecurity/bugmon/commit/751f917f34cf69a3276fb599cc46e423a2bca9bc))

## v1.0.1 (2021-08-06)
### Fix
* Handle failed builds during verification ([`799906f`](https://github.com/MozillaSecurity/bugmon/commit/799906fabd92d07248759e0bf63c2434598e0543))

## v1.0.0 (2021-07-30)
### Feature
* Add ability to iterate over build flags and env variables ([#20](https://github.com/MozillaSecurity/bugmon/issues/20)) ([`db287c5`](https://github.com/MozillaSecurity/bugmon/commit/db287c578bddfed6baba39e722db22bcaac0bd97))
* Always return a short rev from initial_build_id ([`8c9b7e5`](https://github.com/MozillaSecurity/bugmon/commit/8c9b7e516fc98d863b2a7212ba59ae5763aefc61))
* Add ability to force bug confirmation ([#19](https://github.com/MozillaSecurity/bugmon/issues/19)) ([`e641988`](https://github.com/MozillaSecurity/bugmon/commit/e6419887ca72e3f3b41baeb171e03864870a1505))
* Add target iterator for detecting evaluator configuration ([#18](https://github.com/MozillaSecurity/bugmon/issues/18)) ([`7f390d3`](https://github.com/MozillaSecurity/bugmon/commit/7f390d3bcd5da58605543e9636ccec9950f5d9cb))
* Add type annotations throughout ([#16](https://github.com/MozillaSecurity/bugmon/issues/16)) ([`ac70459`](https://github.com/MozillaSecurity/bugmon/commit/ac7045983dd2641f5b399510853e308223b04673))
* Create separate error classes for bug and bugmon ([#15](https://github.com/MozillaSecurity/bugmon/issues/15)) ([`6fccc77`](https://github.com/MozillaSecurity/bugmon/commit/6fccc77b60296100c8ae7d76374941f683affb13))

### Fix
* Continue iterating if build failed ([`24a2c1c`](https://github.com/MozillaSecurity/bugmon/commit/24a2c1cd5bc5970ae15ef389e16f0214b148fc1f))
* Revert repeat count to 10 ([`3a0f3bc`](https://github.com/MozillaSecurity/bugmon/commit/3a0f3bc76f92a952a7c37c877dcecca71c1488d3))
* Include bug number failed baseline message ([`f9d7078`](https://github.com/MozillaSecurity/bugmon/commit/f9d70782adb82274ede9fb81a802f5b954f4796d))
* Don't raise parser.error ([`48c34a8`](https://github.com/MozillaSecurity/bugmon/commit/48c34a812f5453bcb4928ff7f27a9691fdd82d37))
* Ignore phabricator attachments ([`42b33f6`](https://github.com/MozillaSecurity/bugmon/commit/42b33f6536184cd4eb94b0c672e1b03cd8f4b75d))
* Set default repeat and timeout for JSEvaluator ([`7fbccd7`](https://github.com/MozillaSecurity/bugmon/commit/7fbccd7c72a8d810b92ac193b115f4ffc88d2d87))
* Add additional logging for bugs with no matching config ([`dbd7db1`](https://github.com/MozillaSecurity/bugmon/commit/dbd7db158faba18fea608a9ff45b160a7e3c9001))
* Do not cache results when detecting configuration ([`036f28e`](https://github.com/MozillaSecurity/bugmon/commit/036f28e9dadbb7380a8e7f34e7e99ed6c177d757))
* Add additional paths for HG branch revisions ([`9f78759`](https://github.com/MozillaSecurity/bugmon/commit/9f78759ddc5cfd41676647ac0d5b4a2f92d89bcd))
* Treat assertions as debug builds until build flag iterator implemented ([`8c1cdf3`](https://github.com/MozillaSecurity/bugmon/commit/8c1cdf3faeb184fbdde2f66cd276297ec181ff23))
* Update autobisect to fix bug in bisection result message ([`4f33a46`](https://github.com/MozillaSecurity/bugmon/commit/4f33a4697ec20d30489a079182258dbafcd6d3c7))
* Only split env variables based on first equal sign ([`cb8bc0d`](https://github.com/MozillaSecurity/bugmon/commit/cb8bc0dcbab7c51d2f5b0020777866d4462eb63a))

### Breaking
* Bugmon now expects working_dir to be a Path object. ([`8df3391`](https://github.com/MozillaSecurity/bugmon/commit/8df3391624d6868dcdcf1222f768c979cb1252a4))
* Bugmon now expects working_dir to be a Path object. ([`bab8d1e`](https://github.com/MozillaSecurity/bugmon/commit/bab8d1e079e673689d428e21920009dc964cfb7d))
* Individual analysis method names have been renamed, effectively breaking the API. ([`ba44690`](https://github.com/MozillaSecurity/bugmon/commit/ba4469061d0a8313ee972acada7364c2234a6e37))

### Documentation
* Enforce sphinx docstrings ([#17](https://github.com/MozillaSecurity/bugmon/issues/17)) ([`45ff588`](https://github.com/MozillaSecurity/bugmon/commit/45ff588ee4b48b94b60ccdcc0f05ed0bdbe96bc1))

## v0.8.8 (2021-06-21)
### Fix
* Fetcher objects no longer require target arg ([`a60cd0b`](https://github.com/MozillaSecurity/bugmon/commit/a60cd0b986cb51c3be96aac5644988b644ee2ed5))
* Updated autobisect to v1.0.0 due to previous breakage ([`6527994`](https://github.com/MozillaSecurity/bugmon/commit/6527994665a90198680a1f1c287ee80a69a6c90f))

## v0.8.7 (2021-06-21)
### Fix
* Update toml version in lockfile ([`a7154d3`](https://github.com/MozillaSecurity/bugmon/commit/a7154d3e8092850eb918c9eab8432b26451877da))
* Update grizzly-framework and fuzzfetch ([`932bac6`](https://github.com/MozillaSecurity/bugmon/commit/932bac6288779b147ee937e990103279884f02ab))
* Set minimum python version to 3.6.1 ([`3a53536`](https://github.com/MozillaSecurity/bugmon/commit/3a53536ad8555e37ea99706d35fc7f978e716fd4))

### Documentation
* Add readme location to pyproject.toml ([`4c4dd6e`](https://github.com/MozillaSecurity/bugmon/commit/4c4dd6e7a91ae7203b05892f6ff34a2e792d83c3))
