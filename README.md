# Bookmark API

로그인한 사용자가 URL 북마크를 저장하는 FastAPI 예제입니다. 로컬 SQLite, JWT 인증, 요청 로깅, 미들웨어를 사용합니다. Docker는 쓰지 않습니다.

## 실행

```bash
cd bookmark-api
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

문서: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

루트 `/` 는 라우트가 없어서 404가 납니다. `/docs` 또는 `/health`로 확인하세요.

## 사용 순서

1. `POST /register` — 계정 만들기 (예: `alice` / `secret`)
2. 오른쪽 위 **Authorize** — 같은 username / password로 로그인
3. `POST /bookmarks` — URL 저장
4. `GET /bookmarks` — 내 북마크만 조회

`Authorize`는 토큰을 직접 붙이는 칸이 아닙니다. username / password를 넣으면 Swagger가 `/token`을 호출합니다.

## API

| 메서드 | 경로 | 인증 | 설명 |
|--------|------|------|------|
| GET | `/health` | 없음 | 헬스체크 |
| POST | `/register` | 없음 | 회원가입 |
| POST | `/token` | 없음 | JWT 발급 (form: username, password) |
| GET | `/bookmarks` | Bearer | 내 북마크 목록 |
| POST | `/bookmarks` | Bearer | 북마크 생성 (IP당 분당 10회) |
| GET | `/bookmarks/{id}` | Bearer | 단건 조회 |
| PATCH | `/bookmarks/{id}` | Bearer | 수정 |
| DELETE | `/bookmarks/{id}` | Bearer | 삭제 |

같은 사용자가 같은 URL을 두 번 저장하면 400입니다.

## 설정

`.env` 예시:

```env
APP_NAME=Bookmark API
SECRET_KEY=change-me-to-a-long-random-string
DATABASE_URL=sqlite:///./bookmarks.db
DEBUG=true
ALLOWED_HOSTS=["localhost","127.0.0.1"]
```

`@lru_cache` 때문에 프로세스 실행 중에는 처음 읽은 설정을 재사용합니다. `.env`를 바꿨으면 서버를 재시작하세요. `--reload`는 파이썬 파일 변경만 감지합니다.

로컬은 `.env`로 두고, 배포 환경에서는 OS 환경 변수로 넣는 편이 낫습니다. `.env`는 git에 올리지 않습니다.

## 디렉터리

```text
app/
  main.py                 앱 조립, 미들웨어 등록
  api/
    deps.py               Depends (get_current_user)
    router.py             라우트 모음
    routes/               auth, bookmarks, health
  core/                   설정, JWT, 로그, rate limit
  db/                     엔진, 세션, Base
  models/                 SQLAlchemy 테이블
  schemas/                Pydantic 요청/응답
  middleware/             요청 로그, 호스트 검사
```

- SQLAlchemy `models/` — DB에 어떻게 저장하는가
- Pydantic `schemas/` — API로 무엇을 주고받는가

## 로깅

요청 로그는 미들웨어가 남깁니다. 회원가입/로그인 성공·실패는 `api/routes/auth.py`에 따로 있습니다.

```text
POST /bookmarks -> 201 (8.16ms)
```

콘솔과 `app.log`에 동시에 기록됩니다.