# CHANGELOG


## v4.4.1 (2025-02-12)

### Bug Fixes

- Manually update pyproject version
  ([`4b27dcd`](https://github.com/MozillaSecurity/bugmon/commit/4b27dcdf795c1e5e9ff86807697b2f173fbf01bb))

### Continuous Integration

- Disable changelog generation
  ([`a964eba`](https://github.com/MozillaSecurity/bugmon/commit/a964ebabde8537fc741c1a4216b5e1bacfca5bb5))

- Update python-semantic-release commit message config variable
  ([`2823ff6`](https://github.com/MozillaSecurity/bugmon/commit/2823ff627271e8e1b90ed1a2807ebc16d8f8b102))

- Update python-semantic-release configuration
  ([`81987b4`](https://github.com/MozillaSecurity/bugmon/commit/81987b4d9bd284275a7a13b40319788fcb455d32))

- Update python-semantic-release to v9.19.1
  ([`940d030`](https://github.com/MozillaSecurity/bugmon/commit/940d030e949cdd911d276c3e733c3a89fdef1607))


## v4.4.0 (2025-02-12)

### Chores

- Update lockfile
  ([`0c288df`](https://github.com/MozillaSecurity/bugmon/commit/0c288dff448c310e31924810bd71f6e7b86c7870))

### Features

- Update autobisect to v8.1.0
  ([`f2b5a17`](https://github.com/MozillaSecurity/bugmon/commit/f2b5a177782f5dac713e3494205783de747dea0c))


## v4.3.0 (2025-01-22)

### Features

- Use test_info first if it exists
  ([`9922526`](https://github.com/MozillaSecurity/bugmon/commit/9922526d31c65e896eb7d7714ec5c755211d10b1))


## v4.2.4 (2025-01-21)

### Bug Fixes

- Grizzly no longer supports test_info.json as a testcase
  ([`4093584`](https://github.com/MozillaSecurity/bugmon/commit/40935841cea9707304227cdb3c124dfd9b6862ef))

### Chores

- Update lockfile
  ([`55e2ecd`](https://github.com/MozillaSecurity/bugmon/commit/55e2ecd6bbbfdd5b810ba8f469bd64d436a3cdb1))


## v4.2.3 (2025-01-15)

### Bug Fixes

- Add a needinfo instead of redirecting
  ([`e0bc179`](https://github.com/MozillaSecurity/bugmon/commit/e0bc179ff65c4f1be6e668e0efac854cd29d82a2))


## v4.2.2 (2024-12-05)

### Bug Fixes

- Update fuzzfetch and autobisect to latest
  ([`f4390c2`](https://github.com/MozillaSecurity/bugmon/commit/f4390c2f27eddc5b62e4cfe2cb4513bef8271f78))

### Testing

- Record network requests using pytest-recording
  ([`7f48694`](https://github.com/MozillaSecurity/bugmon/commit/7f48694980498256a46bb1fd4d1f73a7899a842e))


## v4.2.1 (2024-12-03)

### Bug Fixes

- Fetcher target param is a list
  ([`a558df7`](https://github.com/MozillaSecurity/bugmon/commit/a558df783b00db2fd867f542debf18bd7ab0d86a))

### Continuous Integration

- Do a full checkout of master for semantic-release
  ([`78e369f`](https://github.com/MozillaSecurity/bugmon/commit/78e369fc13d19a46d40f8ce591dfb7ef690b7ddc))

- Fix semantic-release version_variable
  ([`c00d7f7`](https://github.com/MozillaSecurity/bugmon/commit/c00d7f71265314e107721c88579abb08897b9075))

- Update dev dependencies
  ([`7ed69d0`](https://github.com/MozillaSecurity/bugmon/commit/7ed69d09d7c4b2301e7f4d0f9ed72ed9bfc61471))

- Update semantic release commands and drop version from tox
  ([`8786aa9`](https://github.com/MozillaSecurity/bugmon/commit/8786aa930dc7d948c40f5c52bb6624fed224cb63))


## v4.2.0 (2024-12-03)

### Features

- Update autobisect and fuzzfetch
  ([`d48703f`](https://github.com/MozillaSecurity/bugmon/commit/d48703f16912fb5b8920bbeb1d6c3a57e3530427))


## v4.1.0 (2024-11-12)

### Features

- Check return code of pernosco-submit to determine availability
  ([`efd7f47`](https://github.com/MozillaSecurity/bugmon/commit/efd7f47ee2922a0e6aff57a41013cc9bba26326a))


## v4.0.0 (2024-11-12)

### Bug Fixes

- Revert version and set python minimum version
  ([`2bb6a47`](https://github.com/MozillaSecurity/bugmon/commit/2bb6a47356e187d3344e4831d3f9e5d1aade12fe))

### Chores

- Update lock file
  ([`ca46d15`](https://github.com/MozillaSecurity/bugmon/commit/ca46d15a0544f3a7395319925523f95d308e7d2a))

### Continuous Integration

- Ignore pylint too-many-positional-arguments
  ([`3286b61`](https://github.com/MozillaSecurity/bugmon/commit/3286b61cc16b1c5676d9c586a54ba837b3523183))

- Update orion CI repo
  ([`c9a820d`](https://github.com/MozillaSecurity/bugmon/commit/c9a820d935bac32f13f22e64be38707034870667))

### Features

- Drop support for python 3.8
  ([`e418478`](https://github.com/MozillaSecurity/bugmon/commit/e418478849ab52a80e63099eb233945cd2db43f3))

BREAKING CHANGE: Sets minimum python to version 3.9.

### Breaking Changes

- Sets minimum python to version 3.9.


## v3.8.0 (2024-04-23)

### Bug Fixes

- Remove unnecessary check for pre py3.8 versions
  ([`dec0b50`](https://github.com/MozillaSecurity/bugmon/commit/dec0b5080b6687e1fa578399636a4b99e3fcfbd3))

### Chores

- Update lockfile
  ([`8aa9e3e`](https://github.com/MozillaSecurity/bugmon/commit/8aa9e3e0a9ba17a6b16f9a810b949b1af018fdb9))

### Features

- Set explicit retries and increase backoff_factor
  ([`75341de`](https://github.com/MozillaSecurity/bugmon/commit/75341de8a0f89ad643cab0d435d44e7d2cc512f5))


## v3.7.0 (2024-03-11)

### Features

- Local sources are no longer required for pernosco traces
  ([`87f0b9a`](https://github.com/MozillaSecurity/bugmon/commit/87f0b9a1961531704641f1131f049202a93de051))


## v3.6.2 (2024-01-08)

### Bug Fixes

- Specify encoding when reading file contents
  ([`0a12a4e`](https://github.com/MozillaSecurity/bugmon/commit/0a12a4e20fd3f976dbbd426c50d89203faa77383))


## v3.6.1 (2024-01-02)

### Bug Fixes

- Update autobisect to 7.5.0
  ([`72fce58`](https://github.com/MozillaSecurity/bugmon/commit/72fce58352b72afee397ddb9a8c4cb5be9890f1d))


## v3.6.0 (2023-12-18)

### Features

- Disable headless when running on windows
  ([`e5ccdf5`](https://github.com/MozillaSecurity/bugmon/commit/e5ccdf5e32ac9fe2585c38d1c36df35119c7b5a8))


## v3.5.3 (2023-12-09)

### Bug Fixes

- Remove unused dependencies
  ([`1179adf`](https://github.com/MozillaSecurity/bugmon/commit/1179adfc3f48e6433ccb167fa125209b858cff24))

### Refactoring

- Move to src layout
  ([`5ba62c5`](https://github.com/MozillaSecurity/bugmon/commit/5ba62c5d67601022475a9497ce22a00ec116a1b3))


## v3.5.2 (2023-12-09)

### Bug Fixes

- Apply linter fixes
  ([`c5a9906`](https://github.com/MozillaSecurity/bugmon/commit/c5a9906e545e9d8e94416299bc4c63c3dda62a18))

- Replace typing pipe operator with union
  ([`9a098a6`](https://github.com/MozillaSecurity/bugmon/commit/9a098a66e58e8ca67c30cb9f1b311adb5ad0e73b))

### Continuous Integration

- Move taskcluster_yml_validator to remote hook
  ([`cfdb401`](https://github.com/MozillaSecurity/bugmon/commit/cfdb401522fee0dfa1966de6321368627d4e5d7b))

- Replace isort with flake8
  ([`7e05366`](https://github.com/MozillaSecurity/bugmon/commit/7e0536624cc478f78912c15d147c84c1aed6404f))

- Update ci dependencies and tox configuration
  ([`a7f7bc2`](https://github.com/MozillaSecurity/bugmon/commit/a7f7bc2a53302f0bc3eaa7c13e8df5153f0b64de))


## v3.5.1 (2023-12-09)

### Bug Fixes

- Improve error handling for pernosco recordings
  ([`c78be3e`](https://github.com/MozillaSecurity/bugmon/commit/c78be3e85d8c90bd7c81eb35dedcac96a7a7b66d))

- Only run pernosco on 64-bit Linux bugs
  ([`2287c5d`](https://github.com/MozillaSecurity/bugmon/commit/2287c5d6226c9f0e5c1b0e3218db10623e962221))

- Remove duplicate pernosco credential warning
  ([`a278b8b`](https://github.com/MozillaSecurity/bugmon/commit/a278b8be06a261ea86037b2c19e599589c22ee3f))

### Testing

- Update expected error message
  ([`d720442`](https://github.com/MozillaSecurity/bugmon/commit/d72044269f3b97c26d97230b5027f5aebde9cb33))


## v3.5.0 (2023-12-09)

### Bug Fixes

- Continue iterating over branches even if a patch can't be identified
  ([`cc9f676`](https://github.com/MozillaSecurity/bugmon/commit/cc9f6761568b36b7cbd54ee22edf254878f320bc))

- Update autobisect
  ([`08ee05e`](https://github.com/MozillaSecurity/bugmon/commit/08ee05efccd3e31c4b95628f00f84c85898b382c))

- Use headless in windows
  ([`0480b83`](https://github.com/MozillaSecurity/bugmon/commit/0480b8359cbd1c4d0cbf86964002fa2d91096f4a))

### Features

- Check that affected branches have also been verified
  ([`3e426fc`](https://github.com/MozillaSecurity/bugmon/commit/3e426fcc1907c2dfed7b8f654f051e266d2cb273))

- Verify bugs which still have affected versions associated
  ([`9a82264`](https://github.com/MozillaSecurity/bugmon/commit/9a82264c03196ca6221a62e8b3d8997185ffa599))


## v3.4.3 (2023-12-04)

### Bug Fixes

- Warn when attempting to process non-native bugs
  ([`2c33f05`](https://github.com/MozillaSecurity/bugmon/commit/2c33f057221fc58efe3de0c17540f872f4376b02))


## v3.4.2 (2023-11-28)

### Bug Fixes

- Update autobisect to 7.4.1
  ([`2b87b25`](https://github.com/MozillaSecurity/bugmon/commit/2b87b2509c23c8f09b899259ed299e92e21d91d7))


## v3.4.1 (2023-10-18)

### Bug Fixes

- Notify when pernosco is requested for non 64-bit bugs
  ([`6dfaebd`](https://github.com/MozillaSecurity/bugmon/commit/6dfaebd4919f5e416f1b9ddea3da563adcbb6b94))


## v3.4.0 (2023-10-16)

### Continuous Integration

- Fix action key
  ([`6817e6a`](https://github.com/MozillaSecurity/bugmon/commit/6817e6a1c9f1b2c6588c6005457ba47df4da9ff4))

- Include only expected events and actions in taskcluster.yml
  ([`64119e7`](https://github.com/MozillaSecurity/bugmon/commit/64119e7f8a2b98d33245ea20655477ed6c818966))

- Minor formatting changes
  ([`f47b00d`](https://github.com/MozillaSecurity/bugmon/commit/f47b00df83b28fce45d73bd9c97729c53fa2adca))

- Minor formatting changes
  ([`bb3001c`](https://github.com/MozillaSecurity/bugmon/commit/bb3001cf11d049dc6d85377a537aee2562decebc))

### Features

- Update autobisect to 7.4.0
  ([`85ec8f8`](https://github.com/MozillaSecurity/bugmon/commit/85ec8f86200d5255b04ed699bb5da55af85bcc7a))


## v3.3.0 (2023-10-10)

### Bug Fixes

- Avoid non fuzzing builds as they are tier 2
  ([`47c12aa`](https://github.com/MozillaSecurity/bugmon/commit/47c12aa2309d1e8242589c3481dbd46be00e9aa8))

Tier 2 builds lack a rank in the build info which breaks our build iteration.

### Features

- Update autobisect
  ([`54e50d4`](https://github.com/MozillaSecurity/bugmon/commit/54e50d42f4a10d01e554a340e435183e935cecb7))


## v3.2.1 (2023-10-04)

### Bug Fixes

- Use xvfb as default headless mode
  ([`1beeb04`](https://github.com/MozillaSecurity/bugmon/commit/1beeb04707421942aa05db4dd52f00a603a25af7))


## v3.2.0 (2023-10-04)

### Bug Fixes

- Re-enable use of opt and non-fuzzing builds
  ([`dfc864e`](https://github.com/MozillaSecurity/bugmon/commit/dfc864e7f7660a6c93e2e1bbc0a40227df17a2a8))

- Update autobisect to 7.2.1
  ([`923447e`](https://github.com/MozillaSecurity/bugmon/commit/923447ea0c54985cb437cc63efbcf8cce90bccac))

### Chores

- Update lockfile
  ([`0cfe580`](https://github.com/MozillaSecurity/bugmon/commit/0cfe580c6a67116bba6641b1dd09fc64fd19b5a0))

- Update lockfile
  ([`cd702ca`](https://github.com/MozillaSecurity/bugmon/commit/cd702cabf11a14c1bbd6b8e2ecbe64884a78c799))

### Features

- Simplify product generation
  ([`c526585`](https://github.com/MozillaSecurity/bugmon/commit/c52658598fdaea046ef3ad90481960958f29b3b5))


## v3.1.4 (2023-08-16)

### Bug Fixes

- Update autobisect to fix LD_LIBRARY_PATH issue
  ([`2b154a4`](https://github.com/MozillaSecurity/bugmon/commit/2b154a445437e99f129c288b639a76ab2be6ac60))


## v3.1.3 (2023-08-15)

### Bug Fixes

- Allow non-fuzzing builds in config iterator
  ([`21cff9a`](https://github.com/MozillaSecurity/bugmon/commit/21cff9a76bbf1f6f9879466950c88188b05aeb28))

- Don't check existing bug flags when generating products
  ([`a56aad9`](https://github.com/MozillaSecurity/bugmon/commit/a56aad92b45561209c7cc695a807ffcb6ad68086))

- Update autobisect to set LD_LIBRARY_PATH to build dir for js shell
  ([`630e95e`](https://github.com/MozillaSecurity/bugmon/commit/630e95e512de8e38fcd999e4faab61381033f8b7))

### Build System

- Use poetry group.dev for listing dev dependencies
  ([`128cd9f`](https://github.com/MozillaSecurity/bugmon/commit/128cd9fa6756866cfb8f5b57a1eff9590efdff92))

### Chores

- Update lockfile
  ([`57d11ab`](https://github.com/MozillaSecurity/bugmon/commit/57d11ab6338970f8eadd526fbd70b4008532a4df))

- Update taskcluster-yml-validator
  ([`4c13036`](https://github.com/MozillaSecurity/bugmon/commit/4c13036c13614233b9554565c362185dc024ea97))

### Continuous Integration

- Use python-semantic-release from pyproject.toml
  ([`dc143db`](https://github.com/MozillaSecurity/bugmon/commit/dc143db9ead5ba46a3f67d008e5d3bf47c50bdc0))


## v3.1.2 (2023-07-14)

### Bug Fixes

- Catch failed attempts at fetching builds
  ([`c29532d`](https://github.com/MozillaSecurity/bugmon/commit/c29532de82d7279b025cebefea7879273e2a6e57))

- Expand list of build configurations to avoid
  ([`de44324`](https://github.com/MozillaSecurity/bugmon/commit/de44324b95c8c2ac457441cfbc6798fee87638cd))


## v3.1.1 (2023-06-12)

### Bug Fixes

- Avoid non-fuzzing debug builds now that crashreporter-symbols.zip is no longer indexed
  ([`880baff`](https://github.com/MozillaSecurity/bugmon/commit/880baff111421f2e2c5f6c04d80a47ab84edcb37))

### Testing

- Update config iterator build count
  ([`8d8db10`](https://github.com/MozillaSecurity/bugmon/commit/8d8db10374cd8c0a7c2418cae97d9921911c2361))


## v3.1.0 (2023-06-12)

### Bug Fixes

- Avoid opt builds now that crashreporter-symbols.zip is no longer indexed
  ([`90a8889`](https://github.com/MozillaSecurity/bugmon/commit/90a88895585a44328a0f19bf7e9327a857df0d24))

### Continuous Integration

- Rmeove unnecessary pylint exclusion
  ([`39f0d98`](https://github.com/MozillaSecurity/bugmon/commit/39f0d9831035a877079aebd3f09639de3c1069c4))

### Features

- Add asan to the build flag iterator
  ([`3a44d5f`](https://github.com/MozillaSecurity/bugmon/commit/3a44d5f806d68c13ceb691b2c9b05c33f101c962))

### Testing

- Update build iterator expected result counts
  ([`ca2f3cd`](https://github.com/MozillaSecurity/bugmon/commit/ca2f3cdb060123b28042d3c0d40d9ad42223282a))


## v3.0.2 (2023-06-08)

### Bug Fixes

- Autobisect update includes fix for recent taskcluster build changes
  ([`13f7524`](https://github.com/MozillaSecurity/bugmon/commit/13f752497325e6608df59963d358c539684280d8))


## v3.0.1 (2023-05-03)

### Bug Fixes

- Update autobisect to 7.0.1
  ([`3ab270a`](https://github.com/MozillaSecurity/bugmon/commit/3ab270a22c362a4bc8fd2497c4898ef633df4994))

### Chores

- Update lockfile
  ([`606afd3`](https://github.com/MozillaSecurity/bugmon/commit/606afd3ca53f84dc3f81859e4530786c29b6cdaf))


## v3.0.0 (2023-04-25)

### Build System

- Drop support for python 3.7
  ([`87b5d98`](https://github.com/MozillaSecurity/bugmon/commit/87b5d98d93c012e72adbe3092cb42760c9a5f02a))

BREAKING CHANGE: drop support for python 3.7

- Update minimum poetry version to 1.0.8
  ([`d4d07a6`](https://github.com/MozillaSecurity/bugmon/commit/d4d07a6167be7d2e286beb6b7b7d5c0c7938b1c3))

### Continuous Integration

- Update orion to 0.0.6
  ([`7476b05`](https://github.com/MozillaSecurity/bugmon/commit/7476b05f1f6e7764ed450edb452c9a60b98990ba))

- Update taskcluster test matrix
  ([`418dfdc`](https://github.com/MozillaSecurity/bugmon/commit/418dfdcf7a183bdc7c325d313593f81e6b4b196a))

### Features

- Update autobisect to v7.0.0
  ([`4852dba`](https://github.com/MozillaSecurity/bugmon/commit/4852dba01d4dc8c5a293ff05a3a5b3ead47264f5))


## v2.4.0 (2023-04-14)

### Continuous Integration

- Remove local codecov dependency
  ([`7bfc447`](https://github.com/MozillaSecurity/bugmon/commit/7bfc44738ff1420101482b9fccfc7d8a721bd89f))

### Features

- Add pernosco-failed status command
  ([`b7ae968`](https://github.com/MozillaSecurity/bugmon/commit/b7ae9686c657ef01576cf40903d4f3794cd5f8f9))


## v2.3.2 (2023-03-01)

### Bug Fixes

- Report pernosco-submit error on failure
  ([`3dbd79d`](https://github.com/MozillaSecurity/bugmon/commit/3dbd79d0137cf73fd0cf8a52e75048f4706293c5))


## v2.3.1 (2023-03-01)

### Bug Fixes

- Add punctuation to report messages
  ([`675dbe5`](https://github.com/MozillaSecurity/bugmon/commit/675dbe5e20300576bf642a85bf89dc8d2a62cc53))


## v2.3.0 (2023-02-23)

### Features

- Update pernosco related keywords if trace successful
  ([`e357be2`](https://github.com/MozillaSecurity/bugmon/commit/e357be2c5b2ed495117608c8017327829335a577))

### Testing

- Verify that commands are added to whiteboard
  ([`5561444`](https://github.com/MozillaSecurity/bugmon/commit/5561444bdede770ee7a57748c002ac9d91811204))


## v2.2.0 (2023-02-21)

### Bug Fixes

- Check that command exists before adding or removing it
  ([`17ee883`](https://github.com/MozillaSecurity/bugmon/commit/17ee883b64f5a9201f443ecb5ec809b73a396463))

### Chores

- Update lockfile
  ([`962eb5c`](https://github.com/MozillaSecurity/bugmon/commit/962eb5c5bbd5853d8dab29e6a1f08b47c35f747c))

### Continuous Integration

- Update tox to 4.4.6
  ([`0d37da0`](https://github.com/MozillaSecurity/bugmon/commit/0d37da0de3a2e8e010b0967902ed8b63c24678ce))

### Features

- Replace confirm/verify commands with analyze
  ([`8683418`](https://github.com/MozillaSecurity/bugmon/commit/86834183067a3064f4f44e50bd2704f739f619ef))


## v2.1.4 (2022-12-06)

### Bug Fixes

- Report success on pernosco before upload
  ([`492378f`](https://github.com/MozillaSecurity/bugmon/commit/492378f8471d8ee2a7dfb5ad69736665db0e30f8))


## v2.1.3 (2022-12-01)

### Bug Fixes

- Update fuzzfetch
  ([`4d533ae`](https://github.com/MozillaSecurity/bugmon/commit/4d533ae6b92cc4ac389118e15e3c74f2c5e55c4d))


## v2.1.2 (2022-12-01)

### Bug Fixes

- Log pernosco-submit error message
  ([`784be5c`](https://github.com/MozillaSecurity/bugmon/commit/784be5c38b15826f71f0db0d5577f91357bc913d))


## v2.1.1 (2022-11-30)

### Bug Fixes

- Minor change in bug comment
  ([`3acfef8`](https://github.com/MozillaSecurity/bugmon/commit/3acfef8b96e7029401287725d0ac569d288f71d9))


## v2.1.0 (2022-11-07)

### Features

- Relaunch browser after every attempt
  ([`83f1d19`](https://github.com/MozillaSecurity/bugmon/commit/83f1d1982e1e3a57141f123d51de487e505ee048))


## v2.0.4 (2022-10-28)

### Bug Fixes

- Minor changes to logging and comment output
  ([`d272d3c`](https://github.com/MozillaSecurity/bugmon/commit/d272d3c0e90dd574152bf64e4f64bc0d793ffde9))

- Remove pernosco creds from environment
  ([`78c5898`](https://github.com/MozillaSecurity/bugmon/commit/78c5898ed660cfb489a146dfc3a1f22f433e22ea))

- Require pernosco creds in submit_pernosco
  ([`2949a4c`](https://github.com/MozillaSecurity/bugmon/commit/2949a4cc7e07366236ee70ef10ebe7f31e62f35d))

- Set grizzly time-limit instead of timeout for pernosco sessions
  ([`1344f10`](https://github.com/MozillaSecurity/bugmon/commit/1344f100e6d23b2343f791daa2efdd3a9e3ca0e8))

- Use default timeout for browser evaluator
  ([`b131550`](https://github.com/MozillaSecurity/bugmon/commit/b13155032a436ff513d893755823c533b4daad0e))

### Refactoring

- Apply isort
  ([`5ac8a18`](https://github.com/MozillaSecurity/bugmon/commit/5ac8a188c8d1b2e498cc9ac603628c53c0e4dbca))

- Move PernoscoCreds to utils
  ([`d60202c`](https://github.com/MozillaSecurity/bugmon/commit/d60202cc00a0a8d36d1910fe029fc2a71ca5cbad))

### Testing

- Remove flake8
  ([`91afc92`](https://github.com/MozillaSecurity/bugmon/commit/91afc926a03ca7c5bc40eba757b7cda6579afac5))

- Update expected log message
  ([`a37c920`](https://github.com/MozillaSecurity/bugmon/commit/a37c92073f4d446712f4a55de37cc707fbd1aa98))


## v2.0.3 (2022-10-20)

### Bug Fixes

- Post to bug that pernosco session has been recorded
  ([`bf030c9`](https://github.com/MozillaSecurity/bugmon/commit/bf030c94d189529a9de1f36916c6f6261bfac9dd))


## v2.0.2 (2022-10-20)

### Bug Fixes

- Update path to pernoscoshared lib
  ([`8ac091b`](https://github.com/MozillaSecurity/bugmon/commit/8ac091bd464e760b770af4ef073399316f9beb8b))

### Chores

- Update autobisect
  ([`1674c32`](https://github.com/MozillaSecurity/bugmon/commit/1674c320cf0d70d2dd4cdab0c940dff079df1484))


## v2.0.1 (2022-10-20)

### Bug Fixes

- Update autobisect to ensure log path is set
  ([`4722d0e`](https://github.com/MozillaSecurity/bugmon/commit/4722d0e26324ad23f52be5f1f9e85576761a53df))


## v2.0.0 (2022-10-20)

### Bug Fixes

- Conditionally import typing_extensions for py37
  ([`886f9a3`](https://github.com/MozillaSecurity/bugmon/commit/886f9a33a107003619dcbcb8f624c352e1ac3827))

- Use __name__ when declaring logger
  ([`145f4e5`](https://github.com/MozillaSecurity/bugmon/commit/145f4e5a0312906c3a76603efc555e22f771cb4a))

### Chores

- Update autobisect to v6.0.0
  ([`0789bbc`](https://github.com/MozillaSecurity/bugmon/commit/0789bbce13f4f7948fff75903a099b51681beb2b))

### Documentation

- Minor pydoc updates
  ([`36f9c2e`](https://github.com/MozillaSecurity/bugmon/commit/36f9c2e9196554b96d1295d38cb905ccb3b7cee0))

### Features

- Add support for record pernosco sessions
  ([`778599f`](https://github.com/MozillaSecurity/bugmon/commit/778599fe6bf4228f3376fd0815dd0993ffef3e44))

BREAKING CHANGE: This commit makes numerous changes to the BugMonitor API

- Export BugmonException
  ([`e30804a`](https://github.com/MozillaSecurity/bugmon/commit/e30804a2bb4d51c0b75e51a3a241c39ad2c0c2b7))

### Refactoring

- Explicitly return None
  ([`b073e10`](https://github.com/MozillaSecurity/bugmon/commit/b073e10eec58fe5550a45915f619e7cafff2e12d))

- Lowercase pernosco-submit
  ([`2a17807`](https://github.com/MozillaSecurity/bugmon/commit/2a17807f64ae501a27f5715768f900da7d28974e))

- Remove absolute import path
  ([`44e16ef`](https://github.com/MozillaSecurity/bugmon/commit/44e16efaa0ff703346aa9d0ed8962a687c86f625))

- Remove unnecessary encoding declaration
  ([`78804bd`](https://github.com/MozillaSecurity/bugmon/commit/78804bdfa0fa6e05ba69fba5e36cd082a46fd7fd))

- Remove unnecessary new line
  ([`6225d41`](https://github.com/MozillaSecurity/bugmon/commit/6225d41a4d2ec5b265c469ae48c3398ae2bef2f2))

- Rename and simplify test fixtures
  ([`4f79440`](https://github.com/MozillaSecurity/bugmon/commit/4f79440704903326a64fed57900871c716aca723))

- Use absolute path to utils:
  ([`aff9f66`](https://github.com/MozillaSecurity/bugmon/commit/aff9f66b93a444c7c7ffe04b004444ce4411d156))

### Testing

- Verify pernosco functionality
  ([`18ec03e`](https://github.com/MozillaSecurity/bugmon/commit/18ec03ef67310447cdf2722d5e1707cea8199057))

- Verify pernosco functionality
  ([`6a22f5e`](https://github.com/MozillaSecurity/bugmon/commit/6a22f5e5d068b251e0bb713cc126e5196e83e61e))


## v1.3.2 (2022-09-27)

### Bug Fixes

- Update autobisect to ensure relaunch is set to 1
  ([`695b80f`](https://github.com/MozillaSecurity/bugmon/commit/695b80f7863664b3fc68284a233f1024979180e2))


## v1.3.1 (2022-07-07)

### Bug Fixes

- Remove verify from commands after verification
  ([`e22d8a5`](https://github.com/MozillaSecurity/bugmon/commit/e22d8a59ba5ef2b5aa5f88cdbfa992436dd7cc66))


## v1.3.0 (2022-06-03)

### Bug Fixes

- Add typing_extensions import for py37
  ([`81f6a30`](https://github.com/MozillaSecurity/bugmon/commit/81f6a30409e785fe7d10f76afe533dabd04a3a44))

- Minor reporter formatting changes
  ([`d3a9b2d`](https://github.com/MozillaSecurity/bugmon/commit/d3a9b2d6fa7bb9b4975b2ba97e4f0ee993a0ffae))

### Documentation

- Add comment
  ([`cc8128e`](https://github.com/MozillaSecurity/bugmon/commit/cc8128e20ba77fa3c421529cf3a1fb35c557b7d4))

- Fix indent
  ([`604c0ed`](https://github.com/MozillaSecurity/bugmon/commit/604c0ed33baa7d8542ad92dfbcc4f4538ff32a5e))

### Features

- Add method for setting the needinfo flag
  ([`b097be1`](https://github.com/MozillaSecurity/bugmon/commit/b097be18d8237c6f0dd21a8fcff4db9147797896))

- Add needinfo flag if bug fixed prematurely
  ([`b16fde7`](https://github.com/MozillaSecurity/bugmon/commit/b16fde72b2518a05d62ce4c2e91389dd7896d6e1))

- Add property for retrieving the assignee or creator
  ([`b81bd1b`](https://github.com/MozillaSecurity/bugmon/commit/b81bd1bd77fedeebcf38621d2ffcc0f8a89f461c))

### Testing

- Add bugmon keyword for completeness
  ([`d62c9cd`](https://github.com/MozillaSecurity/bugmon/commit/d62c9cdd9e7a9320cd219e9af0c1119534d45110))

- Add fixture for returning bugmon instance
  ([`79ea363`](https://github.com/MozillaSecurity/bugmon/commit/79ea363cc4acbe3debd988e35dd46168ca75df41))

- Add test for setting ni on premature bug fix
  ([`19479b5`](https://github.com/MozillaSecurity/bugmon/commit/19479b587857879bb4dc1731458a20d551799fc8))

- Add tests for bug assignee and add_needinfo
  ([`04028ff`](https://github.com/MozillaSecurity/bugmon/commit/04028ff8f171073774275573af3d9f8b4e8bdc90))


## v1.2.4 (2022-06-01)

### Bug Fixes

- Exclude nyx builds
  ([`8f17265`](https://github.com/MozillaSecurity/bugmon/commit/8f1726591948a100cad50f5a4866e10577803556))

- Update autobisect to fix fuzzfetch errors
  ([`596646b`](https://github.com/MozillaSecurity/bugmon/commit/596646b3dc052e42d3d3a72029e61d2ea7bd00e3))

### Chores

- Update lockfile
  ([`244ec60`](https://github.com/MozillaSecurity/bugmon/commit/244ec605140fd4061b87953b6e1084b176677736))


## v1.2.3 (2022-04-29)

### Bug Fixes

- Exit early if no fix commit found
  ([`f755a43`](https://github.com/MozillaSecurity/bugmon/commit/f755a43dc07b595e8beb10e5c329bdb4f2f8c46a))

### Chores

- Update autobisect to 5.0.1
  ([`d1c8c78`](https://github.com/MozillaSecurity/bugmon/commit/d1c8c783f95d9d3fd4f6a06adeed743f73581d5f))


## v1.2.2 (2022-04-22)

### Bug Fixes

- Only set status to verified if not new
  ([`b5153ab`](https://github.com/MozillaSecurity/bugmon/commit/b5153ab9baab4d3c16f128f04c7b8ae5db1aba37))


## v1.2.1 (2022-04-04)

### Bug Fixes

- Update autobisect to 3.1.9
  ([`200c7d5`](https://github.com/MozillaSecurity/bugmon/commit/200c7d5c754930d1ead26441f576d84da3a026b3))

- Update autobisect to v5.0.0
  ([`a8bf24c`](https://github.com/MozillaSecurity/bugmon/commit/a8bf24c13e00b281ee8e3439e0534ffbe687de08))

### Chores

- Update lockfile
  ([`fec161b`](https://github.com/MozillaSecurity/bugmon/commit/fec161b88902ecfa9724401bb80e8c86a341e402))

- Update lockfile
  ([`cf38b33`](https://github.com/MozillaSecurity/bugmon/commit/cf38b3357f1bd2f2e80019b581f54822cf50414c))

### Testing

- Run pre-commit via poetry
  ([`bb2c576`](https://github.com/MozillaSecurity/bugmon/commit/bb2c57634215deee61e4493176f6fd0a6c6a748a))


## v1.2.0 (2022-03-02)

### Bug Fixes

- Add free-form params attr for reporting configuration
  ([`299faf1`](https://github.com/MozillaSecurity/bugmon/commit/299faf1f477259a3a2b97f39822807c2e8d4ed82))

- Catch attempts to initialize bisector with an invalid range
  ([`e1e1b06`](https://github.com/MozillaSecurity/bugmon/commit/e1e1b069e03321a0c542b79689d02abc2cf3b649))

- Exclude prefs from possible entry points
  ([`4ff9789`](https://github.com/MozillaSecurity/bugmon/commit/4ff978916ef1ccaf5f81695e20d739d4f09f3e5b))

- Expand failed verification message
  ([`8b23c11`](https://github.com/MozillaSecurity/bugmon/commit/8b23c1123b4d91359b48b8aea04cd8e294768984))

- Fix name for accessibility component
  ([`89ab663`](https://github.com/MozillaSecurity/bugmon/commit/89ab663a2cfcf3d7dd198b33766fc7c8a8f6fa72))

- Identify testcases recursively
  ([`81979a9`](https://github.com/MozillaSecurity/bugmon/commit/81979a98a3e09eb46365d22052139775b665ac1e))

- Remove unused mypy comment
  ([`378fa22`](https://github.com/MozillaSecurity/bugmon/commit/378fa22caddd0f2f3f79bacb4de3abf7c17992a6))

- Set explicit type hint
  ([`1fab91a`](https://github.com/MozillaSecurity/bugmon/commit/1fab91a49ae451d58550b8d208a716dc6eac79da))

- Update autobisect to ignore unhandleable ooms
  ([`ff39c29`](https://github.com/MozillaSecurity/bugmon/commit/ff39c29b5e73dfd124ffdd77bd7730c26532e066))

- Update lockfile to correct breakage in grizzly
  ([`9fc9dfa`](https://github.com/MozillaSecurity/bugmon/commit/9fc9dfa44ae6876ec0e958bb080b36b39b897d46))

### Build System

- Add taskcluster-yml-validator as a local dependency
  ([`83f1e84`](https://github.com/MozillaSecurity/bugmon/commit/83f1e848ce6f4f62faa35e8a06c387fa5809a3f2))

- Bump minimum python version to 3.7
  ([`12b05b8`](https://github.com/MozillaSecurity/bugmon/commit/12b05b8005ca8c099732b0932ae7b09b9ce90e22))

- Update all test dependencies
  ([`3dfabe2`](https://github.com/MozillaSecurity/bugmon/commit/3dfabe2599fe694a1b49f0b69e5f65a8b3d5a824))

### Chores

- Update autobisect
  ([`4714969`](https://github.com/MozillaSecurity/bugmon/commit/47149692e51ac238a8d8d183b476df5c5e651682))

- Update autobisect to v3.1.7
  ([`8544c6d`](https://github.com/MozillaSecurity/bugmon/commit/8544c6d304390cf2c032d8c62c54fc3a276d423e))

- Update lockfile
  ([`8c3682d`](https://github.com/MozillaSecurity/bugmon/commit/8c3682d7028598f14c80b663e1bc9a7c4c5eacae))

### Continuous Integration

- Remove python 3.6 testing
  ([`2092961`](https://github.com/MozillaSecurity/bugmon/commit/2092961bd8a444def15febaa810d70e1ca10e4cb))

- Run poetry install before lint
  ([`e0207ad`](https://github.com/MozillaSecurity/bugmon/commit/e0207ad8e102c277b971e5b8d2838c8179a67dec))

### Documentation

- Fix report pydoc params
  ([`b7bc1f4`](https://github.com/MozillaSecurity/bugmon/commit/b7bc1f4970f307ef5f2de264db9c0049454c4bdf))

### Features

- Add regression keyword if bisection succeeds
  ([`963ca70`](https://github.com/MozillaSecurity/bugmon/commit/963ca7026c491e72f067152461277e6f32236ffe))

### Refactoring

- Minor change to failed bisection message
  ([`bfc7547`](https://github.com/MozillaSecurity/bugmon/commit/bfc754730f1a21b92ac9e1272800e68968609355))

### Testing

- Add lint deps not installed by pre-commit
  ([`598230c`](https://github.com/MozillaSecurity/bugmon/commit/598230cafa117c18b876b01befef0aee49fcd376))

- Convert pre-commit entries to local where applicable
  ([`bbffa2f`](https://github.com/MozillaSecurity/bugmon/commit/bbffa2f31d85906658adc512ec0b6bab8e155092))

- Fix path to pyproject.toml
  ([`a6a1392`](https://github.com/MozillaSecurity/bugmon/commit/a6a1392c0ca0320c77c6cd4dfa31dd6a882ae7df))

- Only run toml-sort on pyproject.toml
  ([`d35643e`](https://github.com/MozillaSecurity/bugmon/commit/d35643ec9e59ae250422bde086ec40511936b683))

- Only trigger pylint and mypy when modifying python files
  ([`4329dc9`](https://github.com/MozillaSecurity/bugmon/commit/4329dc921053bda9e564c141357d68244d963db0))

- Pass files where applicable
  ([`1b6a898`](https://github.com/MozillaSecurity/bugmon/commit/1b6a898585fb8dae96174dbceeb130c272103f2c))

- Remove poetry references from tox
  ([`4291fee`](https://github.com/MozillaSecurity/bugmon/commit/4291feeb4d98d9c53ae854ed4804a9a1fe285390))

- Remove python 3.6 from tox configuration
  ([`7ce8b82`](https://github.com/MozillaSecurity/bugmon/commit/7ce8b82a40e2fb02af05a4af10a3da3362aeb216))


## v1.1.3 (2021-09-01)

### Bug Fixes

- Catch Fetcher errors when artifact doesn't exist
  ([`d010ab8`](https://github.com/MozillaSecurity/bugmon/commit/d010ab839a0fc2af5f8b2a425161b91fb0122e67))

- Filter out directories during testcase iteration
  ([`f9f6270`](https://github.com/MozillaSecurity/bugmon/commit/f9f62708b43c21930e8d058e50e4d7b994ba3c87))

- Improve logging when bug repros on tip but not initial
  ([`9261167`](https://github.com/MozillaSecurity/bugmon/commit/92611676d4693c51707489c1254722ce58d07d15))

- Only close bug if we actually tested the original build
  ([`9ef08f2`](https://github.com/MozillaSecurity/bugmon/commit/9ef08f2014a56d2fd36f4c546b50a5e8a2653d9e))

- Simplify pref detection
  ([`0a12517`](https://github.com/MozillaSecurity/bugmon/commit/0a1251789f3eb411b6801fafe9ef27d07f6d7a5d))

### Refactoring

- Remove unused code that demonstrates routine analysis
  ([`260381c`](https://github.com/MozillaSecurity/bugmon/commit/260381cdffd4ac2639533d6d5902ead726577e51))

The example demonstrated by this code is no longer needed now that --force-confirm has been
  implemented.


## v1.1.2 (2021-08-17)

### Bug Fixes

- Don't yield the same build flags more than once
  ([`fdbf79f`](https://github.com/MozillaSecurity/bugmon/commit/fdbf79f83b1f1519b74d6dbea0fc36a021e3eed8))

### Chores

- Update autobisect
  ([`72c59c0`](https://github.com/MozillaSecurity/bugmon/commit/72c59c056d7fcd5095d85a35209ae2e99fa9f2ff))


## v1.1.1 (2021-08-06)

### Bug Fixes

- Move unnecessary deps to dev-dependencies
  ([`ced1ad8`](https://github.com/MozillaSecurity/bugmon/commit/ced1ad85250c86768001378bec91e001e19d5924))

### Testing

- Run toml-sort recursively
  ([`1d1a867`](https://github.com/MozillaSecurity/bugmon/commit/1d1a867bbc9adda13b5c24034ed4f2f135b6e458))


## v1.1.0 (2021-08-06)

### Bug Fixes

- Only force confirmation if no other action applies
  ([`751f917`](https://github.com/MozillaSecurity/bugmon/commit/751f917f34cf69a3276fb599cc46e423a2bca9bc))

### Features

- Add harness iterator for BrowserEvaluator
  ([#23](https://github.com/MozillaSecurity/bugmon/pull/23),
  [`5d127fb`](https://github.com/MozillaSecurity/bugmon/commit/5d127fbfc0e7b4171dd4f490c6420f5b296b0c7d))

* feat: add harness iterator for BrowserEvaluator

* test: update expected BrowserConfiguration iteration count


## v1.0.1 (2021-08-06)

### Bug Fixes

- Handle failed builds during verification
  ([`799906f`](https://github.com/MozillaSecurity/bugmon/commit/799906fabd92d07248759e0bf63c2434598e0543))

### Chores

- Update autobisect
  ([`706fd47`](https://github.com/MozillaSecurity/bugmon/commit/706fd4794042659157e25c4ce487a33b894d3672))


## v1.0.0 (2021-07-30)

### Bug Fixes

- Add additional logging for bugs with no matching config
  ([`dbd7db1`](https://github.com/MozillaSecurity/bugmon/commit/dbd7db158faba18fea608a9ff45b160a7e3c9001))

- Add additional paths for HG branch revisions
  ([`9f78759`](https://github.com/MozillaSecurity/bugmon/commit/9f78759ddc5cfd41676647ac0d5b4a2f92d89bcd))

- Continue iterating if build failed
  ([`24a2c1c`](https://github.com/MozillaSecurity/bugmon/commit/24a2c1cd5bc5970ae15ef389e16f0214b148fc1f))

- Do not cache results when detecting configuration
  ([`036f28e`](https://github.com/MozillaSecurity/bugmon/commit/036f28e9dadbb7380a8e7f34e7e99ed6c177d757))

- Don't raise parser.error
  ([`48c34a8`](https://github.com/MozillaSecurity/bugmon/commit/48c34a812f5453bcb4928ff7f27a9691fdd82d37))

- Ignore phabricator attachments
  ([`42b33f6`](https://github.com/MozillaSecurity/bugmon/commit/42b33f6536184cd4eb94b0c672e1b03cd8f4b75d))

- Include bug number failed baseline message
  ([`f9d7078`](https://github.com/MozillaSecurity/bugmon/commit/f9d70782adb82274ede9fb81a802f5b954f4796d))

- Only split env variables based on first equal sign
  ([`cb8bc0d`](https://github.com/MozillaSecurity/bugmon/commit/cb8bc0dcbab7c51d2f5b0020777866d4462eb63a))

- Revert repeat count to 10
  ([`3a0f3bc`](https://github.com/MozillaSecurity/bugmon/commit/3a0f3bc76f92a952a7c37c877dcecca71c1488d3))

- Set default repeat and timeout for JSEvaluator
  ([`7fbccd7`](https://github.com/MozillaSecurity/bugmon/commit/7fbccd7c72a8d810b92ac193b115f4ffc88d2d87))

- Treat assertions as debug builds until build flag iterator implemented
  ([`8c1cdf3`](https://github.com/MozillaSecurity/bugmon/commit/8c1cdf3faeb184fbdde2f66cd276297ec181ff23))

- Update autobisect to fix bug in bisection result message
  ([`4f33a46`](https://github.com/MozillaSecurity/bugmon/commit/4f33a4697ec20d30489a079182258dbafcd6d3c7))

### Build System

- Update autobisect to v2.0.0 ([#14](https://github.com/MozillaSecurity/bugmon/pull/14),
  [`8df3391`](https://github.com/MozillaSecurity/bugmon/commit/8df3391624d6868dcdcf1222f768c979cb1252a4))

* refactor: use pathlib where applicable

BREAKING CHANGE: Bugmon now expects working_dir to be a Path object.

* build: update autobisect to v2.0.0

* fix: pass target to BuildManager.get_build()

### Chores

- Update ffpuppet
  ([`205b839`](https://github.com/MozillaSecurity/bugmon/commit/205b839e9e429107427efd6b0e1da839f1e8ed5b))

- Update prefpicker
  ([`92f769a`](https://github.com/MozillaSecurity/bugmon/commit/92f769a6592a1f15c2ad176216b95cf98ab087e0))

### Code Style

- Minor output change
  ([`3dcd858`](https://github.com/MozillaSecurity/bugmon/commit/3dcd858d0cbcaf81b97bd4ae0120b3961f20639c))

- Minor reformatting
  ([`5a7e81c`](https://github.com/MozillaSecurity/bugmon/commit/5a7e81c1a3ff214b0c802c615bdae72e1db17295))

### Documentation

- Enforce sphinx docstrings ([#17](https://github.com/MozillaSecurity/bugmon/pull/17),
  [`45ff588`](https://github.com/MozillaSecurity/bugmon/commit/45ff588ee4b48b94b60ccdcc0f05ed0bdbe96bc1))

### Features

- Add ability to force bug confirmation ([#19](https://github.com/MozillaSecurity/bugmon/pull/19),
  [`e641988`](https://github.com/MozillaSecurity/bugmon/commit/e6419887ca72e3f3b41baeb171e03864870a1505))

* feat: add ability to force bug confirmation

* fix: disable auto-nag on bug confirmation

- Add ability to iterate over build flags and env variables
  ([#20](https://github.com/MozillaSecurity/bugmon/pull/20),
  [`db287c5`](https://github.com/MozillaSecurity/bugmon/commit/db287c578bddfed6baba39e722db22bcaac0bd97))

* fix: add optional Bugsy type to EnhancedBug

* fix: don't assume build is debug if assertion keyword present

* feat: add ability to iterate over build flags and env variables

* test: add tests for bug configurations

* fix: don't set flags that have already been set

- Add target iterator for detecting evaluator configuration
  ([#18](https://github.com/MozillaSecurity/bugmon/pull/18),
  [`7f390d3`](https://github.com/MozillaSecurity/bugmon/commit/7f390d3bcd5da58605543e9636ccec9950f5d9cb))

- Add type annotations throughout ([#16](https://github.com/MozillaSecurity/bugmon/pull/16),
  [`ac70459`](https://github.com/MozillaSecurity/bugmon/commit/ac7045983dd2641f5b399510853e308223b04673))

* feat: add type annotations throughout

* test: enable mypy as a pre-commit hook

* fix: address mypy violations

* style: sort pyproject.toml

* fix: add py.typed per pep-561

* test: add pylint pre-commit check

* test: enable mypy strict checks

* feat: lock fuzzfetch to 1.3.3

* fix: address mypy strict violations

- Always return a short rev from initial_build_id
  ([`8c9b7e5`](https://github.com/MozillaSecurity/bugmon/commit/8c9b7e516fc98d863b2a7212ba59ae5763aefc61))

- Create separate error classes for bug and bugmon
  ([#15](https://github.com/MozillaSecurity/bugmon/pull/15),
  [`6fccc77`](https://github.com/MozillaSecurity/bugmon/commit/6fccc77b60296100c8ae7d76374941f683affb13))

BREAKING_CHANGE: This may affect Bugmon consumers who rely on the exception instance type.

### Refactoring

- Mark individual analysis methods as private
  ([#12](https://github.com/MozillaSecurity/bugmon/pull/12),
  [`ba44690`](https://github.com/MozillaSecurity/bugmon/commit/ba4469061d0a8313ee972acada7364c2234a6e37))

* refactor: mark individual analysis methods as private

BREAKING CHANGE: Individual analysis method names have been renamed, effectively breaking the API.

* style: re-order Bugmon class methods

- Use pathlib where applicable ([#13](https://github.com/MozillaSecurity/bugmon/pull/13),
  [`bab8d1e`](https://github.com/MozillaSecurity/bugmon/commit/bab8d1e079e673689d428e21920009dc964cfb7d))

BREAKING CHANGE: Bugmon now expects working_dir to be a Path object.

### Testing

- Initial_build_id always returns a short rev
  ([`51e26ff`](https://github.com/MozillaSecurity/bugmon/commit/51e26ff00884dd4b6d13c2b9a6685e20fd522460))

- Pass CODECOV_TOKEN to tox environment
  ([`0145073`](https://github.com/MozillaSecurity/bugmon/commit/0145073fab2a9fbb2073893eb939c4b645c4dedc))

### Breaking Changes

- Bugmon now expects working_dir to be a Path object.


## v0.8.8 (2021-06-21)

### Bug Fixes

- Fetcher objects no longer require target arg
  ([`a60cd0b`](https://github.com/MozillaSecurity/bugmon/commit/a60cd0b986cb51c3be96aac5644988b644ee2ed5))

- Updated autobisect to v1.0.0 due to previous breakage
  ([`6527994`](https://github.com/MozillaSecurity/bugmon/commit/6527994665a90198680a1f1c287ee80a69a6c90f))


## v0.8.7 (2021-06-21)

### Bug Fixes

- Set minimum python version to 3.6.1
  ([`3a53536`](https://github.com/MozillaSecurity/bugmon/commit/3a53536ad8555e37ea99706d35fc7f978e716fd4))

This is required to match the same requirements in autobisect

- Update grizzly-framework and fuzzfetch
  ([`932bac6`](https://github.com/MozillaSecurity/bugmon/commit/932bac6288779b147ee937e990103279884f02ab))

This update is required as grizzly-framework did not previously pin the version of ffpuppet to use.
  An API change in ffpuppet has caused the previously used version of grizzly-framework to fail.

- Update toml version in lockfile
  ([`a7154d3`](https://github.com/MozillaSecurity/bugmon/commit/a7154d3e8092850eb918c9eab8432b26451877da))

### Chores

- Update lockfile
  ([`4b98bc9`](https://github.com/MozillaSecurity/bugmon/commit/4b98bc9089a82c6ccb673a2a2fb2867457aac6c6))

### Code Style

- Apply black formatting
  ([`f8de493`](https://github.com/MozillaSecurity/bugmon/commit/f8de4938a3673bd862e9154770a75d97af833f94))

- Sort import order
  ([`bbceab9`](https://github.com/MozillaSecurity/bugmon/commit/bbceab999eb1c02338d12f7c393eafa054983811))

- Sort pyproject.toml
  ([`0f43426`](https://github.com/MozillaSecurity/bugmon/commit/0f43426f0fe43ffa9a35a81dd86867cecbdc7819))

### Documentation

- Add readme location to pyproject.toml
  ([`4c4dd6e`](https://github.com/MozillaSecurity/bugmon/commit/4c4dd6e7a91ae7203b05892f6ff34a2e792d83c3))

### Testing

- Add gitlint pre-commit hook
  ([`792567f`](https://github.com/MozillaSecurity/bugmon/commit/792567f240ecd94b4d112e559f9d4f90fdab81be))

- Add toml-sort pre-commit hook
  ([`979c8fa`](https://github.com/MozillaSecurity/bugmon/commit/979c8fae36efd82e3c14b3b14af3055c9556f11f))

- Sort pyproject in-place during pre-commit
  ([`804bd63`](https://github.com/MozillaSecurity/bugmon/commit/804bd63f9a0e5bd653942afd9840df37870bbba8))

- Toml-sort does not allow in-place modification as a hook
  ([`145d929`](https://github.com/MozillaSecurity/bugmon/commit/145d9291026d50eec2e927e8e0d4f183cb180347))

- Update toml to fix failing tests on python3.6
  ([`ffa9b46`](https://github.com/MozillaSecurity/bugmon/commit/ffa9b4674476b5b697fc8d57fad3c0e8bebeb85f))


## v0.8.6 (2020-11-30)


## v0.8.5 (2020-10-28)


## v0.8.4 (2020-10-20)


## v0.8.3 (2020-10-20)


## v0.8.2 (2020-10-16)


## v0.8.1 (2020-09-11)


## v0.8.0 (2020-09-02)


## v0.7.1 (2020-06-24)
