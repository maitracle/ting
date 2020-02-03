# ting


## 개발환경 설정
### postgresql 설치
```
$ brew install postgresql

$ echo '# for postgresql' >> ~/.zprofile
$ echo 'export PATH="/usr/local/opt/krb5/bin:$PATH"' >> ~/.zprofile
$ echo 'export PATH="/usr/local/opt/krb5/sbin:$PATH"' >> ~/.zprofile

$ pg_ctl -D /usr/local/var/postgres start
$ export PGDATA='/usr/local/var/postgres'
$ pg_ctl status

$ initdb /usr/local/var/postgres

$ createuser --interactive --pwprompt
# role 이름: root
# superuser

$ createuser --interactive --pwprompt
# role 이름: postgres
# 모든 권한 주지 않음

$ psql -U postgres
postgres=> CREATE DATABASE hongaeting_test;

$ psql -U root -d hongaeting_test
hongaeting_test=# ALTER ROLE postgres CREATEDB;

```

### trouble shooting
```
# db client 관련 문제
# https://stackoverflow.com/questions/44084846/cannot-connect-to-the-docker-daemon-on-macos
env LDFLAGS="-I/usr/local/opt/openssl/include -L/usr/local/opt/openssl/lib" pip install psycopg2==2.8.4
```

#### pyenv 설치 (with pyenv-installer)
```
$ curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash
$ exec $SHELL
```

#### trouble shooting
```
# $ curl https://pyenv.run | bash 가 제대로 동작하지 않음
```

#### ~/.zprofile 파일 가장 아래 아래의 명령어 추가 후 $ source ~/.zprofile
```
# for pyenv
export PATH="/Users/${user-account-name}/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```

#### 가상환경 설정
```
$ pyenv install 3.7.4

$ pyenv virtualenv 3.7.4 {project-name}-env

$ mkdir {project-name}

$ cd /{project-name}

$ pyenv local {project-name}-env
```

#### django 세팅 
```
$ git pull https://github.com/maitracle/ting.git

$ pip install --upgrade pip

$ pip install -r requirements.txt

$ cd hongaeting

$ python manage.py migreate
```

#### 환경변수 설정
```
repository root directory에 .env 파일을 추가한다.
파일 내용은 동료에게 개인적으로 전달받는다.
```

#### run
```
$ python manage.py runserver 0.0.0.0:8000
```
