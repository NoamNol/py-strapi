# Changelog

All notable changes to this project will be documented in this file. See
[Conventional Commits](https://conventionalcommits.org) for commit guidelines.

## [4.3.0](https://github.com/NoamNol/py-strapi/compare/v4.2.0...v4.3.0) (2022-07-04)


### Features

* add custom Strapi errors ([f9c748c](https://github.com/NoamNol/py-strapi/commit/f9c748c4c31af228f2e422bbebbd16e443932bc9))
* add InternalServerError exception ([1f35dac](https://github.com/NoamNol/py-strapi/commit/1f35dacc1b9d0de35baa003796bf57525843e217))
* change Connector interface to only include request() ([21c6c34](https://github.com/NoamNol/py-strapi/commit/21c6c346da7b4ec27a292656021c509b0f19811d))
* don't export helpers from __init__ ([a9e8c9d](https://github.com/NoamNol/py-strapi/commit/a9e8c9df1e1c56d1bf3b9bfa1f0c208e4b647a6f))
* raise custom RatelimitError ([4a4f82f](https://github.com/NoamNol/py-strapi/commit/4a4f82f3c9cd092b41e4838df3f5ce027278423f))
* use raise_for_response in the default connectors ([e4cda98](https://github.com/NoamNol/py-strapi/commit/e4cda98be9a52c3cc324b5526c6ca05c9e453e63))


### Bug Fixes

* add data, error and message to StrapiAuthResponse ([0863153](https://github.com/NoamNol/py-strapi/commit/08631536220ee9b54b3283cd47f21ba6863d95f4))
* pagination methods can not be mixed ([1bb3173](https://github.com/NoamNol/py-strapi/commit/1bb31737a3b14ce4fdc90dc548caa4e2d9c1c1f8))

## [4.2.0](https://github.com/NoamNol/py-strapi/compare/v4.1.0...v4.2.0) (2022-06-27)


### Features

* export connectors and enums ([321bbcc](https://github.com/NoamNol/py-strapi/commit/321bbcc093833365814e4a57138807901dcec97b))


### Bug Fixes

* fix session in connectors ([62f342b](https://github.com/NoamNol/py-strapi/commit/62f342bed3e4f650e37cb7dccfade9251054dc48))

## [4.1.0](https://github.com/NoamNol/py-strapi/compare/v4.0.0...v4.1.0) (2022-06-26)


### Features

* rename StrapiConnector to Connector ([01037de](https://github.com/NoamNol/py-strapi/commit/01037dec304a1a85d0f761bd197350ea7c203f6d))

## [4.0.0](https://github.com/NoamNol/py-strapi/compare/v3.1.1...v4.0.0) (2022-06-25)


### ⚠ BREAKING CHANGES

* rename baseurl to api_url
* remove token parameter from authorize()
* implement StrapiClientSync with requests lib and enable custom Connector

### Features

* add Filter enum ("$eq", "$lt"...) ([7b5eada](https://github.com/NoamNol/py-strapi/commit/7b5eada41c22cd99e637ce4d77ecebc9b706eee8))
* add optional token parameter to Strapi clients ([3e2e797](https://github.com/NoamNol/py-strapi/commit/3e2e797115597035470e79ec94f3d51e9cbe6f09))
* add Strapi type hints ([11236da](https://github.com/NoamNol/py-strapi/commit/11236daa49b0d7c10770ff70d4707427a03625ae))
* enable custom Connector in StrapiClient ([e533f1f](https://github.com/NoamNol/py-strapi/commit/e533f1f06a77c6efb8936caede1a14179ea8c0ab))
* handle bad response in upsert_entry() ([57c1ad8](https://github.com/NoamNol/py-strapi/commit/57c1ad8f5988cbd7511781ad072834116805c16f))
* handle missing "jwt" in response ([2bcc1d4](https://github.com/NoamNol/py-strapi/commit/2bcc1d4b6658cbcfcb228a3e7110af3c107d94ab))
* implement StrapiClientSync with requests lib and enable custom Connector ([81b6b00](https://github.com/NoamNol/py-strapi/commit/81b6b00c4be7e5ae0e1549a4dfb984684a87b0d2))
* improve DefaultStrapiConnector error message ([dadadb6](https://github.com/NoamNol/py-strapi/commit/dadadb6b85dad6a558aaf7ed9656080e88a6dfbe))
* remove token parameter from authorize() ([795fb8b](https://github.com/NoamNol/py-strapi/commit/795fb8b1fdbd7d918700fa00e76c422339d9932d))
* rename baseurl to api_url ([a1df5a1](https://github.com/NoamNol/py-strapi/commit/a1df5a1f128fcea7c53882b38c7e7f8cf6cf75d5))


### Bug Fixes

* fix unsupported urllib3 in python 3.10 ([0dd0af5](https://github.com/NoamNol/py-strapi/commit/0dd0af5ff680ed4de23e3d29a9a5059d0d93e8e0))

### [3.1.1](https://github.com/NoamNol/py-strapi/compare/v3.1.0...v3.1.1) (2022-06-20)


### Bug Fixes

* fix return type to support python 3.8 ([18a3a44](https://github.com/NoamNol/py-strapi/commit/18a3a44675f799baf084d8cbbcac75470face83b))

## [3.1.0](https://github.com/NoamNol/py-strapi/compare/v3.0.0...v3.1.0) (2022-06-20)


### Features

* add baseurl property to StrapiClientSync ([b36071a](https://github.com/NoamNol/py-strapi/commit/b36071a4e8194db8f75f9724b3e35c8002442044))

## [3.0.0](https://github.com/NoamNol/py-strapi/compare/v2.5.0...v3.0.0) (2022-06-19)


### ⚠ BREAKING CHANGES

* init pystrapi fork (#1)

### Features

* init pystrapi fork ([#1](https://github.com/NoamNol/py-strapi/issues/1)) ([a4eb6e1](https://github.com/NoamNol/py-strapi/commit/a4eb6e10a26908879d68fc3389ca331160fe858c))
