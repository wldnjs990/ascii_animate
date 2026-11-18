# 영상 → 실시간 ASCII 애니메이션 웹 서비스의 기술적 타당성 (2026년 11월 기준)

> 조사일: 2026-11-18. 출처 표기 규칙: "(열람)"은 원문 페이지를 직접 읽은 것, "(검색 스니펫)"은 검색 결과 요약만 확인하고 원문은 열람하지 않은 것. 스니펫 기반 항목은 신뢰도를 한 단계 낮게 봐야 한다.
> 법률/저작권/YouTube 약관은 범위 밖이며, 기술적으로 가능하지만 그 판단에 좌우되는 지점만 "[약관/법률 의존]"으로 표시했다.

## 1. 영상 프레임 → ASCII 변환 기법과 기존 오픈소스 프로젝트

### Takeaway
기본 기법(셀 평균 휘도 → 문자 램프 매핑)은 단순하고 브라우저에서 실시간 처리가 쉬우며, 2026년 현재 품질 차별화 요소는 "글리프 형태(shape) 매칭 + 대비 강화"를 GPU 셰이더로 돌리는 방식이다. 브라우저용 오픈소스(collidingScopes/ascii, textmode.js, p5.asciify, aalib.js, ASCILINE 등)가 이미 다수 존재해 변환 자체는 새로 발명할 필요가 없다.

### Cited Findings

**기법**
- 표준 방식은 각 문자 셀을 "픽셀 1개"로 취급해 밝기만 매핑하므로 문자 형태를 무시하고 경계가 흐릿해진다. Alex Harri는 셀의 국소 형태에 가장 잘 맞는 문자를 고르는 shape-vector 방식을 제안했다(2026-01-17 게시). — [alexharri.com, "ASCII characters are not pixels"](https://alexharri.com/blog/ascii-rendering) (열람)
- 해당 방식의 구체 내용: 문자마다 6개의 엇갈린 샘플링 원에 대한 잉크 겹침 비율로 6차원 shape vector를 사전 계산하고, 프레임의 각 셀에서도 같은 6개 원의 평균 명도(상대 휘도)를 샘플링해 유클리드 최근접 문자를 찾는다. 2차원(상/하 2원)으로는 `p`/`q` 같은 문자를 구분하지 못해 6차원으로 확장했다. — [alexharri.com](https://alexharri.com/blog/ascii-rendering) (열람)
- 조회 가속: k-d tree, 그리고 6개 성분을 각 5비트(32단계)로 양자화해 하나의 정수 키로 묶는 캐시. 캐시를 전부 채우면 GB 단위가 필요하지만 lazy 채움으로 실용적이며, MacBook에서 수천 건 조회가 수 ms 수준이라고 기술. — [alexharri.com](https://alexharri.com/blog/ascii-rendering) (열람)
- 대비 강화: (a) 전역 — 샘플 벡터를 최대 성분으로 정규화 후 지수 적용, (b) 방향성 — 셀 바깥 10개의 외부 샘플링 원으로 이웃 셀 값을 읽어 경계의 계단 현상을 제거. GPU 구현은 6개 셰이더 패스(내부 샘플 수집 → 외부 샘플 수집 → 외부 최댓값 → 방향성 강화 → 내부 최댓값 → 전역 강화). — [alexharri.com](https://alexharri.com/blog/ascii-rendering) (열람)
- 성능 서술: 초기 CPU 프로토타입은 iPhone에서 한 자릿수 FPS였고, 병목은 조회가 아니라 샘플링이었다. 샘플링과 강화를 GPU로 옮겨 "몇 배" 빨라졌다고 하나 정확한 배수/그리드 수치는 열람본에서 확인되지 않았다. 2차 요약 기사에서는 GPU 방식으로 약 60 FPS에 도달했다고 전한다. — [alexharri.com](https://alexharri.com/blog/ascii-rendering) (열람); [news.lavx.hu 요약 기사](https://news.lavx.hu/article/ascii-characters-are-not-pixels-a-deep-dive-into-ascii-rendering) (검색 스니펫)
- 일반적 브라우저 파이프라인은 "프레임을 오프스크린 canvas에 그림 → 픽셀 읽기 → 셀을 문자로 매핑"이며, WebGL로 밝기 계산을 오프로드할 수 있다. — [OpenReplay blog](https://blog.openreplay.com/ascii-art-browser-terminal/) (검색 스니펫)
- 단순성과 효율 때문에 구조 기반 대신 밝기 매핑을 의도적으로 택한 셰이더 기반 플레이어 사례도 있다. — [Ascii Video Player (cafebot)](https://cafebot.pages.dev/Ascii-Video-Player) (검색 스니펫)

**브라우저용 오픈소스/라이브러리**
- collidingScopes/ascii: JS + HTML canvas로 영상을 ASCII 픽셀 아트로 변환, MIT 라이선스, 웹캠 또는 업로드한 영상 입력, 색/해상도/텍스트 스타일 조절. 라이브 데모 collidingscopes.github.io/ascii. — [awesome.ecosyste.ms 항목](https://awesome.ecosyste.ms/projects/github.com%2Fcollidingscopes%2Fascii) (검색 스니펫); [Show HN](https://hn.nuxt.dev/item/41389326) (검색 스니펫)
- aalib.js (mir3z): 이미지와 동영상을 ASCII 아트로 변환하는 순수 JS 브라우저 라이브러리, 스트림 방식 처리. 유지보수 활성 여부는 확인하지 못했다. — [github.com/mir3z/aalib.js](https://github.com/mir3z/aalib.js/) (검색 스니펫)
- Asciify (sister-software): 이미지/영상/3D 렌더를 래스터화된 ASCII로 변환하는 소형 라이브러리. DOM 텍스트 노드 대신 canvas에 직접 래스터화하므로 훨씬 빠르다고 저자가 주장. — [github.com/sister-software/asciify](https://github.com/sister-software/asciify/blob/v3.1.3/) (검색 스니펫)
- textmode.js: `<canvas>`나 `<video>` 요소를 동적 ASCII 표현으로 바꾸는 WebGL 라이브러리. — [unpkg README](https://app.unpkg.com/textmode.js@0.1.3/files/README.md) (검색 스니펫)
- p5.asciify: p5.js용 실시간 ASCII 효과 라이브러리. — [p5.asciify README](https://cdn.jsdelivr.net/npm/p5.asciify@0.10.3/README.md) (검색 스니펫)
- react-video-ascii: WebGL2로 라이브 영상을 canvas에 렌더하는 React 컴포넌트. 휘도 모드 외에 글리프 실루엣을 모서리/엣지 특징과 비교하는 `shape` 모드 제공. — [react-video-ascii 소개 페이지](https://kn86-docs-gca3d.kinsta.page/influences/effect/react-video-ascii/) (검색 스니펫)
- video-stream-ascii (Im-Rises): React/JS npm 패키지 + 웹 데모(웹캠, 임의의 비디오 스트림). — [github.com/Im-Rises/video-stream-ascii-player](https://github.com/Im-Rises/video-stream-ascii-player) (검색 스니펫)
- AuraASCII: GPU에서 edge-aware 알고리즘으로 실시간 영상 변환하는 오픈소스 도구(Product Hunt 소개). — [Product Hunt](https://www.producthunt.com/p/auraascii) (검색 스니펫)
- ASCILINE: 서버(Python/FastAPI, OpenCV 또는 선택적 Rust/FFmpeg 엔진) + 브라우저 canvas 플레이어 구조의 "ASCII video rendering engine". 코어 엔진/스트리밍 서버는 AGPL-3.0-or-later, 클라이언트 SDK와 웹 디코더(`asciline-player`, `codec.js`)는 MIT. ASCII 모드 1–6(흑백 ~ 1,600만 색)과 컬러 블록 `--pixel` 모드. — [github.com/YusufB5/ASCILINE](https://github.com/YusufB5/ASCILINE) (열람)

### Inferences
- 변환 품질 단계는 (1) 휘도 램프 → (2) 컬러 ASCII(문자는 휘도, 색은 셀 평균 RGB) → (3) 디더링/엣지 검출 → (4) 6D shape-vector 매칭 순으로 비용이 오른다. (1)~(2)는 CPU로도 충분하고, (4)를 영상 해상도 그리드에 적용하려면 사실상 GPU 셰이더가 필요하다(Harri 글의 "샘플링이 병목" 서술에 근거).
- ASCILINE의 서버 코어가 AGPL이므로, 이를 서버에 그대로 가져다 쓰는 네트워크 서비스는 소스 공개 의무 검토가 필요하다. MIT인 collidingScopes/ascii나 자체 구현이 라이선스 부담이 적다. [약관/법률 의존 — 라이선스 해석은 별도 확인 필요]
- 디더링(Floyd–Steinberg, ordered/Bayer)을 ASCII에 적용하는 기법 자체는 널리 쓰이지만, 이번 조사에서 디더링만 다룬 1차 출처는 열람하지 못했다.

### Gaps
- 휘도 매핑 vs shape 매칭을 같은 하드웨어에서 비교한 정량 벤치마크는 찾지 못했다(검색 결과에도 없다고 명시됨).
- 각 라이브러리의 최신 커밋 날짜, 스타 수, 유지보수 상태는 직접 확인하지 않았다. textmode.js, p5.asciify, react-video-ascii의 라이선스도 미확인.
- Alex Harri 글의 정확한 벤치마크 수치(그리드 크기, ms, k-d tree 배수)는 열람본에서 누락되어 보고하지 못한다.

---

## 2. 파일 업로드 경로: 브라우저 클라이언트 단독 처리 가능 여부

### Takeaway
가능하다. 사용자가 고른 로컬 파일은 `blob:` URL로 same-origin 취급되어 canvas 오염이 없고, `<video>` + `requestVideoFrameCallback` + canvas/WebGL 조합만으로 서버 없이 실시간 ASCII 변환과 오디오 동기화가 된다. 오디오는 `<video>` 요소가 그대로 재생하고 ASCII는 "현재 표시되는 프레임"에서 매번 파생되므로 구조적으로 싱크가 어긋나기 어렵다.

### Cited Findings

**프레임 획득과 동기화**
- `requestVideoFrameCallback`(rVFC)은 새 비디오 프레임이 합성에 제출될 때마다 콜백을 실행하고 `mediaTime`(프레임의 미디어 타임스탬프, 초), `presentedFrames`(누적 제출 프레임 수 — 콜백 사이에 놓친 프레임 탐지 가능), `expectedDisplayTime`, `processingDuration`, `width`/`height` 등의 메타데이터를 준다. — [web.dev, rVFC](https://web.dev/articles/requestvideoframecallback-rvfc) (열람)
- "프레임을 재현 가능하게 정확히 식별하려면 `mediaTime`을 써야 한다"고 명시. — [web.dev](https://web.dev/articles/requestvideoframecallback-rvfc) (열람)
- 한계: API 전체가 best effort이며 엄격한 보장이 없다. 실제 렌더 시점보다 1 vsync 늦을 수 있다. 콜백 실행률은 영상 프레임률과 브라우저(디스플레이) 주사율 중 낮은 쪽으로 제한된다(25fps 영상 + 60Hz → 25Hz). 프레임 정확 seek는 보장되지 않으며 그런 작업은 WebCodecs를 쓰라고 안내. — [web.dev](https://web.dev/articles/requestvideoframecallback-rvfc) (열람)
- rVFC 지원: Chrome 83, Edge 83, Firefox 132, Safari 15.4. — [web.dev](https://web.dev/articles/requestvideoframecallback-rvfc) (열람)
- web.dev 데모 자체가 콜백 안에서 현재 프레임을 canvas에 그리고 콜백을 재등록하는 패턴이다. — [web.dev](https://web.dev/articles/requestvideoframecallback-rvfc) (열람)

**canvas 픽셀 읽기 보안**
- CORS 승인 없이 다른 origin에서 온 데이터를 canvas에 그리는 순간 canvas는 tainted 상태가 되고, 이후 `getImageData()`, `toBlob()`, `toDataURL()`, `captureStream()` 호출은 `SecurityError`를 던진다. `drawImage()` 자체는 성공한다. — [MDN, CORS-enabled image / tainted canvas](https://developer.mozilla.org/en-US/docs/Web/HTML/How_to/CORS_enabled_image) (열람)
- 다른 origin 리소스를 읽으려면 서버가 `Access-Control-Allow-Origin` 헤더를 주고 클라이언트가 `crossOrigin` 속성을 지정해야 한다. — [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/How_to/CORS_enabled_image) (열람)

**WebCodecs / ffmpeg.wasm**
- WebCodecs는 Chromium(Chrome/Edge/Opera)에서 Chrome 94부터 지원. Safari와 Firefox 지원 시점은 출처가 충돌한다: Digital Samba(2026-08)는 "Safari 26.4가 출시된 2026년 3월에 Baseline 도달, Firefox는 2023년부터"라고 하고, Storm Streaming(2026-06)은 "Safari 26.0(2025년 말)에서 전체 지원"이라 하며, 2026-04의 다른 가이드는 "Firefox는 2026년 초 기준 미지원"이라고 한다. Mozilla의 WebCodecs 추적 버그(1746557)는 여전히 open 상태. — [Digital Samba](https://www.digitalsamba.com/blog/webcodecs-api-explained) (검색 스니펫); 상충: [Storm Streaming](https://www.stormstreaming.com/blog/?p=430) (검색 스니펫), [floatleft 가이드](https://floatleftinteractive-project.pages.dev/guides/implementing-webcodecs-in-browser-for-streaming-apps-2026/) (검색 스니펫), [Bugzilla 1746557](https://bugzilla.mozilla.org/show_bug.cgi?id=1746557) (검색 스니펫)
- 코덱별 지원이 다르므로 가정하지 말고 `VideoDecoder.isConfigSupported()`로 런타임 탐지하라는 권고. — [Storm Streaming](https://www.stormstreaming.com/blog/?p=430) (검색 스니펫)
- ffmpeg.wasm: 입력 파일 크기 한계 2GB가 GitHub 이슈로 보고되어 있고(해결 여부 미확인), MEMFS(메모리 내 임시 파일시스템)를 써서 wasm 힙이 차면 훨씬 작은 파일에서도 탭이 죽는 사례가 보고됨. — [ffmpeg.wasm issue #623](https://github.com/ffmpegwasm/ffmpeg.wasm/issues/623) (검색 스니펫); [Hashnode 사례 글](https://hashnode.com/posts/how-i-built-a-zero-server-file-converter-that-digests-1-5-gb-videos-in-the-browser-and-where-it-broke/6aaa99a4f903689d1d3aa0db) (검색 스니펫)
- Mediabunny(WebCodecs 기반 라이브러리) 자체 벤치마크: 691 MiB 1080p 파일을 320x180 WebM으로 변환할 때 Mediabunny 804 frames/s vs ffmpeg.wasm 12.0 frames/s (Ryzen 7600X + RTX 4070). 벤더 자체 수치이므로 독립 검증 필요. — [mediabunny.dev](https://mediabunny.dev/) (검색 스니펫)
- WebCodecs 지원이 파편화되어 있어(특히 구형 Safari) ffmpeg.wasm을 폴백으로 둔 개발 사례가 있다. — [Remotion docs / 관련 글](https://www.remotion.dev/docs/webcodecs/misconceptions) (검색 스니펫)

**현실적 프레임률/그리드 (프로젝트 보고치)**
- ASCILINE: ASCII 재생은 24–30 FPS에 맞춰 튜닝, 권장 ASCII 열 수 200–240(기본 200), 픽셀 모드 600–900(기본 450). 60fps급 소스는 보간 없이 프레임을 솎아낸다. Chrome GPU를 끈 상태에서도 30 FPS 유지했다고 README가 주장(조건은 PERFORMANCE.md, 저자 자체 보고). — [ASCILINE](https://github.com/YusufB5/ASCILINE) (열람)
- ASCILINE: 그리드가 기기에 비해 너무 크면 영상이 오디오보다 뒤처지며, 해결책은 열 수(`--cols`)를 줄이는 것. — [ASCILINE](https://github.com/YusufB5/ASCILINE) (열람)
- Harri: 휴대폰은 노트북보다 프레임당 문자 조회 예산이 몇 배 낮다고 서술. — [alexharri.com](https://alexharri.com/blog/ascii-rendering) (열람)

### Inferences
- 업로드 파일은 `URL.createObjectURL(file)`로 만든 `blob:` URL을 `<video>`에 물리면 페이지와 같은 origin으로 취급되어 tainted canvas 문제가 발생하지 않는다(MDN의 오염 규칙이 "다른 origin + CORS 미승인"에만 적용된다는 점에서 도출. blob URL의 same-origin 취급 자체는 이번 조사에서 별도 출처를 열람하지 않은 일반 지식).
- 권장 1차 아키텍처: `<video>`(숨김 또는 1px, 오디오는 그대로 재생) → rVFC 콜백 → 소형 canvas(그리드 해상도, 예: 160x90)에 `drawImage` 다운스케일 → `getImageData` 또는 WebGL 셰이더로 문자 인덱스 계산 → canvas에 글리프 아틀라스로 그리기. 싱크는 "오디오 = 마스터 클럭(video element), ASCII = 현재 프레임의 파생물"이므로 별도 타임스탬프 정렬 로직이 필요 없다. 처리 지연이 생기면 프레임이 건너뛰어질 뿐 누적 드리프트는 생기지 않는다. `presentedFrames`로 드롭률을 계측할 수 있다.
- 그리드가 160x90(14,400셀) 수준이면 휘도 매핑의 연산량은 셀당 몇 번의 산술이므로 CPU JS로도 30fps가 충분할 것으로 추정된다. 병목은 계산보다 "출력" 쪽일 가능성이 크다: DOM `<pre>`의 textContent를 매 프레임 교체하면(특히 셀별 색상 `<span>`) 레이아웃 비용이 크고, canvas `fillText`나 WebGL 글리프 아틀라스 렌더가 훨씬 유리하다(Asciify 저자의 "DOM 텍스트 노드보다 canvas 래스터화가 훨씬 빠르다"는 주장과 일치). 단, 이 추정에 대한 독립 벤치마크는 확보하지 못했다.
- WebCodecs/ffmpeg.wasm은 실시간 재생에는 필수가 아니다. 필요한 경우는 (a) 프레임 정확한 오프라인 사전 렌더/내보내기, (b) `<video>`가 재생 못 하는 컨테이너/코덱(MKV, 일부 HEVC 등) 지원이다. ffmpeg.wasm은 느리고 메모리 한계가 있어 "폴백 디먹서/트랜스코더" 용도로만 적합하다.
- 브라우저가 디코딩하지 못하는 코덱의 파일은 클라이언트 단독 경로에서 실패하므로, 서버 트랜스코딩 폴백을 둘지 여부가 제품 결정 사항이 된다.
- 백그라운드 탭에서는 rVFC/rAF가 스로틀되어 ASCII 갱신이 멈추지만 오디오는 계속되며, 탭 복귀 시 현재 프레임에서 즉시 재개된다(일반 브라우저 동작에 대한 추정).

### Gaps
- 브라우저에서 "N열 × M행 그리드, 컬러 ASCII, 기기 X에서 몇 FPS"를 측정한 독립 벤치마크를 찾지 못했다. 위 수치는 프로젝트 저자 보고치와 추론이다. 실기기 프로토타입 측정이 필요하다.
- OffscreenCanvas + Worker로 변환을 메인 스레드 밖으로 옮겼을 때의 이득, WebGPU 구현 사례의 성능 수치는 조사하지 못했다.
- WebCodecs의 Safari/Firefox 지원 상태는 출처가 충돌하므로 MDN 호환성 표나 caniuse로 재확인해야 한다.
- 모바일 Safari에서의 autoplay/사용자 제스처 제약, 저전력 모드 시 rVFC 동작은 확인하지 않았다.

---

## 3. YouTube 링크 경로: IFrame 임베드 픽셀 접근 불가와 대안들

### Takeaway
웹 페이지는 YouTube IFrame 임베드의 픽셀을 읽을 수 없다. cross-origin iframe이라 내부 `<video>`에 접근 자체가 차단되고, IFrame Player API는 재생 제어만 제공한다. 남는 대안은 (a) 서버에서 yt-dlp로 받아 처리, (b) 사용자 화면 캡처(getDisplayMedia), (c) 브라우저 확장, (d) 사용자가 직접 받은 파일 업로드인데, (a)는 2025–2026년 YouTube의 PO 토큰 / SABR / JS 챌린지 / 데이터센터 IP 차단 때문에 운영 안정성이 낮고 프록시 비용이 든다.

### Cited Findings

**왜 임베드 픽셀을 못 읽는가**
- YouTube 임베드 iframe의 `contentWindow`를 통해 내부 `<video>`에 접근해 `drawImage`하려던 시도는 브라우저가 cross-origin DOMException으로 차단했고, "다른 origin의 iframe 내용과는 직접 상호작용할 수 없다"는 답변이 달렸다. — [Stack Overflow 56299995 (미러)](https://kiwix.lema.org/stackoverflow.com_en_all_2023-11/questions/56299995/youtube-player-api-get-screenshot) (검색 스니펫, 오래된 Q&A이나 same-origin policy는 변하지 않음)
- IFrame Player API는 "웹사이트에 YouTube 플레이어를 임베드하고 JavaScript로 플레이어를 제어"하는 API로, 큐/재생/일시정지/볼륨 등 제어 기능이며 프레임 데이터를 노출하지 않는다. — [YouTube IFrame Player API Reference](https://developers.google.com/youtube/iframe_api_reference) (검색 스니펫)
- 설령 미디어 URL을 직접 `<video>`에 물릴 수 있다 해도, CORS 승인 없는 cross-origin 콘텐츠를 canvas에 그리면 tainted가 되어 `getImageData()` 등이 `SecurityError`를 던진다. — [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/How_to/CORS_enabled_image) (열람)

**대안 A — 서버 측 yt-dlp 다운로드 [약관/법률 의존]**
- PO(Proof of Origin) 토큰: YouTube가 일부 클라이언트의 요청에 요구하는 파라미터. 없으면 "해당 클라이언트의 포맷 URL 요청이 HTTP 403을 반환하거나 계정 또는 IP 주소가 차단될 수 있다." 토큰은 Web/Android/iOS의 attestation 제공자가 생성하며 플랫폼 간 호환되지 않는다. — [yt-dlp wiki, PO Token Guide](https://github.com/yt-dlp/yt-dlp/wiki/PO-Token-Guide) (열람, 페이지 표기 "edited Jul 12, 2026")
- 클라이언트별 요구(위 가이드의 표): `web`은 Subs와 GVS에 토큰 필요 + SABR 포맷만 제공; `mweb`, `tv_simply`, `web_music`, `web_creator`는 GVS에 필요; `web_safari`는 GVS에 필요하나 HLS 포맷은 현재 불필요; `android`/`ios`는 GVS 또는 Player; `tv`, `web_embedded`, `android_vr`은 불필요. 단 `tv`는 쿠키(로그인 또는 활성 게스트)를 넘기지 않으면 포맷이 전부 DRM 보호되고 일부 경우 SABR 전용, `android_vr`은 "Made for kids" 영상 불가, `web_creator`는 계정 쿠키 필수. — [PO Token Guide](https://github.com/yt-dlp/yt-dlp/wiki/PO-Token-Guide) (열람)
- 권장 구성: "PO Token Provider 플러그인으로 `mweb` 클라이언트에 GVS용 PO 토큰을 공급". 수동 추출은 더 이상 권장되지 않는데, 토큰이 이제 video ID에 바인딩되어 영상마다 새 토큰이 필요하기 때문. 토큰 수명은 짧게는 12시간. 제공 플러그인: bgutil-ytdlp-pot-provider, yt-dlp-getpot-wpc(브라우저에서 YouTube를 띄워 발급하는 폴백) — 둘 다 yt-dlp 공식 소속이 아님. — [PO Token Guide](https://github.com/yt-dlp/yt-dlp/wiki/PO-Token-Guide) (열람)
- SABR: YouTube 자체 스트리밍 프로토콜. 2025-02-26 이슈 개설 시점에 WEB 클라이언트 응답에서 `adaptiveFormats`의 직접 URL이 사라지고 SABR URL만 남기 시작했고, 2025-04-29에는 web 클라이언트의 HTTPS 포맷이 전부 제거되어 SABR만 남았다. yt-dlp의 SABR 다운로더는 개발 중(PR #13515 open)이라고 했으며 이슈는 2025-08-21 기준 잠김. — [yt-dlp issue #12482](https://github.com/yt-dlp/yt-dlp/issues/12482) (열람; 2025년 정보이며 이후 진행 상황은 미확인)
- 2026년 이슈 보고에서도 web / web_safari 클라이언트에 SABR이 강제되고 있다고 언급. — [yt-dlp issue #15897](https://github.com/yt-dlp/yt-dlp/issues/15897) (검색 스니펫)
- JS 런타임 필수화: yt-dlp는 YouTube의 JavaScript 챌린지를 풀기 위해 외부 JS 런타임이 필요하다. EJS(yt-dlp-ejs)가 기존 JSInterp/PhantomJS 방식을 대체했다. 지원 런타임: Deno ≥ 2.3.0(권장, 기본 활성), Node ≥ 22.0.0, Bun 1.2.11–1.3.14(deprecated), QuickJS ≥ 2023-12-9(2025-4-26 이전 빌드는 실행에 수 분이 걸릴 수 있음). yt-dlp-ejs는 yt-dlp와 함께 업데이트해야 한다. — [yt-dlp wiki, EJS](https://github.com/yt-dlp/yt-dlp/wiki/EJS) (열람, wiki 개정일 2026-07-12)
- 레이트 리밋: 게스트 세션은 시간당 약 300개 영상(약 1,000 webpage/player 요청), 계정은 시간당 약 2,000개 영상(약 4,000 요청). 초과 시 "This content isn't available, try again later". 다운로드 사이 5–10초 지연 권장. 계정 쿠키 사용 시 "계정이 (일시 또는 영구) 차단될 위험이 있다." — [yt-dlp wiki, Extractors](https://github.com/yt-dlp/yt-dlp/wiki/Extractors) (열람; 최종 편집 2025-06-11로 표시 — 오래된 수치일 수 있음)
- 데이터센터 IP 차단 실사례(2026-03 게시): Alibaba Cloud 2 vCPU 서버에서 유효한 쿠키를 넣어도 "ERROR: Sign in to confirm you're not a bot"가 발생했고 같은 명령이 가정용 ISP IP에서는 성공. 저자는 YouTube가 쿠키 확인 전에 IP 평판으로 데이터센터 IP를 거부한다고 결론. 시도한 방법 중 public Cobalt API(Turnstile CAPTCHA 요구), self-hosted Cobalt, RapidAPI류 다운로더는 모두 실패했고 **residential 프록시 + yt-dlp(+쿠키)만 성공**. — [dev.to, osovsky](https://dev.to/osovsky/i-was-building-a-cloud-video-service-youtube-turned-me-into-an-ip-trafficker-1l9o) (열람; 단일 개인의 경험담, 정량 실패율 없음)
- 같은 글의 비용: residential 프록시 2GB 플랜 월 $12, 종량제 $3.50/GB. 17분 1080p 영상이 약 400MB. — [dev.to, osovsky](https://dev.to/osovsky/i-was-building-a-cloud-video-service-youtube-turned-me-into-an-ip-trafficker-1l9o) (열람)
- VPN 출구 서버도 같은 프롬프트를 유발하며 5–15개 서버를 바꿔야 풀리는 경우가 있다는 포럼 보고. — [VideoHelp forum](https://forum.videohelp.com/showthread.php?p=2790779) (검색 스니펫)
- 제3자 트러블슈팅 페이지는 2026-08-17에 다수 사용자가 403 오류를 겪기 시작했다고 주장하나 공식 출처로 확인되지 않았다. — [winxdvd 가이드](https://www.winxdvd.com/streaming-video/yt-dlp-not-working-fixed.htm) (검색 스니펫, 미확인 주장)

**대안 B — getDisplayMedia 화면/탭 캡처**
- 캡처 시작 전 브라우저가 사용자에게 공유 요청 확인과 공유 대상 선택을 요구하고, 캡처 중에는 표시(indicator)가 뜬다. `display-capture` Permissions Policy가 필요하다. — [MDN, Using the Screen Capture API](https://developer.mozilla.org/en-US/docs/Web/API/Screen_Capture_API/Using_Screen_Capture) (열람)
- MDN은 이 기능이 "가장 널리 쓰이는 일부 브라우저에서 동작하지 않아 Baseline이 아니다"라고 표기. 오디오 캡처는 항상 선택 사항이며, 오디오를 요청해도 반환 스트림에 비디오 트랙만 있을 수 있다. — [MDN](https://developer.mozilla.org/en-US/docs/Web/API/Screen_Capture_API/Using_Screen_Capture) (열람)
- Chrome 데스크톱: `systemAudio`는 Chrome 105, `displaySurface`/`surfaceSwitching`/`selfBrowserSurface`는 Chrome 107, `monitorTypeSurfaces`는 Chrome 119. 탭 오디오는 "Chrome Tab" 패널에서만 제공되고 "Entire Screen"에서는 제공되지 않는다. `selfBrowserSurface`의 기본값은 현재 "exclude"(현재 탭을 목록에서 제외)이며 `preferCurrentTab: true`와 상호 배타적. 해당 문서에서 Firefox/Safari는 이 옵션들 미지원으로 표시. — [Chrome for Developers, screen sharing controls](https://developer.chrome.com/docs/web-platform/screen-sharing-controls) (열람)

**대안 C/D — 기존 도구들이 쓰는 방식**
- 터미널 ASCII YouTube 플레이어들은 사실상 전부 yt-dlp(또는 구 youtube-dl)로 스트림을 얻는다(4절 참고). — [tplay](https://docs.rs/crate/tplay/0.9.3/source/README.md), [asciitube](https://github.com/PKD667/asciitube), [ascii-live](https://pypi.org/project/ascii-live/) (검색 스니펫)

### Inferences
- "YouTube 임베드를 화면에 띄우지 않고 ASCII만 보여주기"는 순수 웹 페이지에서는 불가능하다. 차단 계층이 여러 겹이다: (1) same-origin policy로 iframe DOM 접근 불가, (2) IFrame API는 postMessage 기반 제어 채널일 뿐 픽셀/스트림을 주지 않음, (3) googlevideo 미디어 URL은 서명되어 있고 CORS 헤더가 제3자 origin에 열려 있지 않아 직접 `<video crossOrigin>`으로 물릴 수 없음(이 부분은 일반 지식에 의한 추정이며 이번 조사에서 1차 출처로 확인하지 않음), (4) 일부 콘텐츠/클라이언트는 DRM(EME) 경로로 제공되어 디코딩된 프레임이 보호 경로에 머물고 canvas로 읽으면 검은 화면이 된다(PO Token Guide의 "`tv` 포맷이 쿠키 없이는 전부 DRM"이라는 서술이 DRM 적용 확대를 뒷받침; EME 프레임 판독 불가 자체는 일반 지식).
- 스트림 프록시(서버가 googlevideo 스트림을 중계하며 CORS 헤더를 붙여 클라이언트가 디코딩)는 기술적으로 대안 A와 같은 추출 단계(yt-dlp 계열)를 필요로 하므로 차단 리스크가 동일하고, 여기에 영상 전체 트래픽의 서버 대역폭 비용이 추가된다. 또한 포맷 URL은 요청 IP에 묶이는 경우가 많아 서버가 추출한 URL을 클라이언트가 직접 쓰기 어렵다(일반 지식, 미확인). [약관/법률 의존]
- 대안별 기술 신뢰도(2026년 말 기준 종합 판단):
  - **서버 yt-dlp + 사전 렌더**: 동작은 하지만 "유지보수 부채가 상시 발생"하는 경로. 필요한 것 = 최신 yt-dlp + yt-dlp-ejs + Deno/Node 런타임 + PO 토큰 제공 플러그인 + (데이터센터에서는 거의 필수로) residential 프록시. YouTube 측 변경으로 수 주 단위 장애가 반복된 이력(2025년 SABR 전환, 2026년 403 보고)이 있어 SLA를 약속하기 어렵다. 게스트 세션 시간당 약 300개 영상 한도도 규모 확장의 상한이 된다.
  - **getDisplayMedia**: 추출 차단과 무관하게 동작한다(브라우저가 이미 합성한 화면을 사용자가 자발적으로 공유). 대신 UX 비용이 크다 — 매번 권한 프롬프트와 탭 선택, 데스크톱 Chromium 중심(탭 오디오 포함), 모바일 사실상 불가, 원본 영상이 어딘가 실제로 렌더되고 있어야 함(다른 탭이나 창), 캡처 해상도/프레임률 변동. "원본 화면은 안 보이게"라는 요구와 부분적으로 충돌한다(다른 탭에 원본이 떠 있어야 함). 캡처 스트림을 `<video>`에 물려 canvas로 읽는 것은 로컬 MediaStream이라 오염되지 않을 것으로 보이나 MDN 해당 문서에는 명시가 없어 프로토타입 검증 필요. DRM 보호 영상은 캡처 시 검게 나올 수 있다.
  - **브라우저 확장**: youtube.com 페이지에 content script를 주입하면 페이지와 같은 origin에서 `<video>` 요소를 canvas에 그려 읽을 수 있어(동일 origin의 MSE 재생이므로 오염 없음 — 일반 지식에 의한 추정) 기술적으로 가장 안정적이고 서버 비용이 0이다. 그러나 "웹 서비스"가 아니라 설치형 제품이 되고, 스토어 심사와 모바일 미지원이 제약이다. [약관/법률 의존]
  - **사용자 로컬 다운로드 후 업로드**: 서비스 입장에서는 2절의 파일 업로드 경로와 동일해 기술 리스크가 0이며, 추출의 부담과 책임이 사용자 쪽으로 이동한다.
- 따라서 기술 리스크 순으로는 "파일 업로드(낮음) < 확장 프로그램 < 화면 캡처 < 서버 yt-dlp(높음, 지속 운영비)"이다.

### Gaps
- yt-dlp의 SABR 다운로더가 2026년 11월 현재 정식 릴리스에 포함되었는지 확인하지 못했다(이슈 #12482는 2025-08 잠김 이후 정보 없음, PR #13515 상태 미확인).
- "데이터센터 IP는 차단된다"에 대한 yt-dlp 공식 문서의 직접 서술은 찾지 못했다(PO Token Guide와 Extractors wiki 모두 언급 없음). 근거는 개인 블로그와 포럼 보고뿐이며 정량 실패율(예: AWS/GCP IP의 성공률)은 없다.
- googlevideo 응답의 CORS 헤더 구성, 포맷 URL의 IP 바인딩 여부를 1차 출처로 확인하지 못했다.
- YouTube가 일반 영상에 Widevine DRM을 어느 범위까지 적용 중인지(2026년 현재 web 클라이언트 기준) 확인하지 못했다. 이것이 확대되면 확장/화면 캡처 경로도 영향을 받는다.
- Invidious/Piped 같은 대체 프런트엔드 인스턴스를 소스로 쓰는 방안의 2026년 가용성은 조사하지 않았다.
- 모바일 브라우저의 getDisplayMedia 지원 표(MDN 호환성 표)를 직접 확인하지 못했다.

---

## 4. 서버 측 파이프라인: 사전 계산, 데이터 크기, 압축, 전송, 비용

### Takeaway
서버에서 ffmpeg로 프레임을 뽑아 ASCII 프레임을 미리 계산하고 오디오와 함께 내려보내는 구조는 ASCILINE이 이미 구현/공개한 검증된 패턴이다. 다만 ASCII 프레임 데이터는 비압축 시 원본 MP4보다 커지므로 델타/zlib/RLE/DCT 같은 프레임 간 압축이 필수이고, 업로드 파일에 한해서는 클라이언트 처리(2절)가 서버 비용 없이 같은 결과를 내므로 서버 파이프라인의 실익은 "YouTube 링크 지원"과 "저사양 기기 지원"에 한정된다.

### Cited Findings
- ASCILINE 구조: 백엔드(Python/FastAPI)가 OpenCV(또는 선택적 Rust/FFmpeg 엔진)로 디코딩 → 픽셀을 문자/컬러 셀로 매핑 → WebSocket으로 바이너리 프레임 스트리밍. 프런트엔드(vanilla JS)는 프레임 수신 → jitter buffer → canvas 그리드 렌더. 스트림 시작 전 `INIT` 메시지로 해상도와 FPS를 협상. — [ASCILINE](https://github.com/YusufB5/ASCILINE) (열람)
- 정적 경로: `compiler.py`가 자체 완결형 `.ascf`(ASCII Compressed Format) 파일을 만들고, 정적 HTML 플레이어가 백엔드 없이 재생한다. — [ASCILINE](https://github.com/YusufB5/ASCILINE) (열람)
- 프레임 인코딩: 프레임당 1바이트 태그로 RAW / ZLIB / DELTA / RLE_FULL / DCT 중 가장 작은 것을 인코더가 선택. 컴파일러 옵션으로 `--quantize`, `--profile`(DCT, 손실), `--qf`, `--tolerance`, `--hard`(최대 zlib). 손실 temporal delta(`--quality`)는 어려운 케이스를 약 15–30% 더 줄인다고 README가 기술. — [ASCILINE](https://github.com/YusufB5/ASCILINE) (열람)
- 크기/대역폭(저자 보고): mode 6, 200×80 그리드에서 정적 콘텐츠는 레거시 대비 약 0.3%, 고모션 콘텐츠는 63% 크기. 라이브 DCT 픽셀 모드는 약 0.1 MB/s vs raw 약 20 MB/s(일반 장면에서 100–250배, 고모션에서 약 50배 절감). README는 "컴파일된 `.ascf` 파일은 본질적으로 표준 `.mp4`보다 크다"고 명시. — [ASCILINE](https://github.com/YusufB5/ASCILINE) (열람)
- 서버 처리 속도(저자 보고, 단일 Windows 머신 / 단일 클라이언트): Rust 엔진으로 59.94 FPS 소스, 464×256 그리드에서 약 60 FPS 전달, 서버 프레임 생성 평균 약 7ms, 브라우저 DCT 디코드 약 2ms. Python DCT는 `--cols 320`에서 프레임당 약 24ms, `--cols 450`에서 약 43ms. 다중 클라이언트 용량은 미검증이라고 README가 인정. — [ASCILINE](https://github.com/YusufB5/ASCILINE) (열람)
- 오디오 싱크: 오디오 트랙을 마스터 클럭("the absolute time reference")으로 삼아 A/V를 맞춘다. — [ASCILINE](https://github.com/YusufB5/ASCILINE) (열람)
- YouTube 입력 처리 방식: yt-dlp(선택적 extra)로 URL을 가져오고, 다운로드는 480p로 상한, video ID로 `videos/`에 캐시, H.264/AAC 고정 프레임률로 정규화, LRU 캐시 한도 기본 10240 MB(`--cache-limit`). 저자는 5–10분 이하의 짧은 클립 컴파일을 권장. — [ASCILINE](https://github.com/YusufB5/ASCILINE) (열람); [HN reader 미러](https://hn.jakechampion.name/reader/https://github.com/YusufB5/ASCILINE) (검색 스니펫)
- 프록시 트래픽 비용 참고치: residential 프록시 $3.50/GB(종량제), 17분 1080p ≈ 400MB. — [dev.to, osovsky](https://dev.to/osovsky/i-was-building-a-cloud-video-service-youtube-turned-me-into-an-ip-trafficker-1l9o) (열람)

### Inferences
- 비압축 크기 산술(자체 계산): 흑백 ASCII 160×90 그리드 = 14,400셀 × 1바이트 = 14.4KB/프레임 → 30fps에서 432KB/s ≈ 26MB/분. 컬러(문자 1바이트 + RGB 3바이트 = 4바이트/셀)면 57.6KB/프레임 → 1.73MB/s ≈ 104MB/분. 4분짜리 뮤직비디오 하나가 비압축 컬러로 약 415MB이므로 압축 없이는 전송이 비현실적이다. 문자 집합이 10~70종이면 셀당 4~6비트로 줄고, gzip/zstd와 프레임 델타로 정적 장면은 크게 줄어든다(ASCILINE의 0.3%~63% 보고치와 방향 일치).
- 핵심 통찰: ASCII 프레임은 "저해상도 영상"의 결정적 함수다. 따라서 가장 효율적인 "ASCII 데이터 전송 포맷"은 사실 그리드 해상도로 다운스케일한 일반 영상(예: 160×90 H.264/VP9/AV1, 수십~수백 kbps)이고, 클라이언트가 이를 디코딩해 ASCII로 변환하면 된다. 서버가 자체 origin(또는 CORS 허용 CDN)에서 이 초소형 영상 + 오디오를 서빙하면 canvas 오염이 없고, 2절의 클라이언트 파이프라인을 그대로 재사용하며, 싱크도 `<video>` 요소가 처리한다. 사전 계산 ASCII 포맷(.ascf류)보다 저장/전송 비용이 훨씬 작다. 손실 압축으로 인한 블록 노이즈가 문자 선택을 흔들 수 있으나 그리드 해상도로 직접 인코딩하면 영향이 작을 것으로 추정(미검증).
- 서버 사전 렌더 ASCII(텍스트 스트림)가 유리한 경우: 클라이언트가 영상 디코딩을 못 하는 환경(터미널, curl, 초저사양), 또는 고비용 변환(6D shape 매칭 + 방향성 대비)을 서버 GPU/CPU에서 한 번만 하고 캐시해 여러 사용자에게 재사용하는 경우.
- 서버 비용 구조(YouTube 경로): (1) 추출/다운로드 — residential 프록시 트래픽이 지배적. 그리드용으로 144p~360p만 받으면 영상당 수 MB~수십 MB로 줄어 $3.50/GB 기준 영상당 대략 $0.01~0.1 수준으로 추정(자체 계산, 실제 최저 포맷 비트레이트에 따라 달라짐), (2) ffmpeg 다운스케일 트랜스코딩 — 저해상도라 CPU 초 단위, (3) 저장/egress — 초소형 영상이라 미미, (4) video ID 기준 캐시로 인기 영상 중복 제거. 운영 인력(추출기 장애 대응)이 실질적인 최대 비용일 가능성이 높다.
- 스케일 상한: 게스트 세션 시간당 약 300개 영상 한도(Extractors wiki, 2025년 수치)를 감안하면 IP/세션 풀 관리가 필요해지고, 이는 곧 프록시 풀 운영을 의미한다.
- 전송 방식 선택지: (a) 초소형 영상 파일을 일반 HTTP range/HLS로 서빙(가장 단순, CDN 캐시 가능), (b) 사전 계산 ASCII 청크를 HTTP로 분할 다운로드 + `audio.currentTime` 기준으로 프레임 인덱스 선택(프레임 인덱스 = floor(currentTime × fps)), (c) WebSocket 라이브 스트림 + jitter buffer(ASCILINE 방식 — seek과 CDN 캐시에 불리). 사전 계산 프레임을 쓸 때의 싱크는 반드시 오디오 클럭을 기준으로 프레임을 "선택"해야 하며 setInterval로 프레임을 "진행"시키면 드리프트가 생긴다.

### Gaps
- 사전 계산 ASCII 포맷과 "초소형 영상 + 클라이언트 변환" 방식의 크기/품질을 직접 비교한 자료는 찾지 못했다. 위 비교는 추론이다.
- 클라우드 단가(컴퓨트/egress)에 기반한 영상당 총비용의 실측 사례를 찾지 못했다. 프록시 단가는 단일 블로그 글의 한 벤더 가격이다.
- ASCILINE의 수치는 모두 저자 자체 보고이며 단일 머신/단일 클라이언트 조건이다. 동시 접속 스케일 자료는 없다.

---

## 5. 유사 프로젝트/서비스와 그들의 영상 소스 확보 방식

### Takeaway
"YouTube 링크 → ASCII 재생"을 하는 기존 프로젝트는 대부분 로컬 터미널 도구이며 거의 전부 사용자 PC에서 yt-dlp를 실행해 소스를 얻는다(가정용 IP라 차단을 덜 받음). 브라우저 기반 ASCII 플레이어는 웹캠/업로드 파일을 입력으로 받는 것이 일반적이고, 호스팅된 웹 서비스가 YouTube 링크를 직접 받는 사례는 이번 조사에서 ASCILINE(셀프호스팅 서버 + yt-dlp) 외에는 확인되지 않았다.

### Cited Findings
- mpv: `--vo=tct`는 유니코드 LOWER HALF BLOCK 문자를 기본 알고리즘으로 써서 세로 해상도를 높이는 터미널 비디오 출력. `--vo=caca`는 mpv가 libcaca 지원으로 빌드되어야 하며 배포판 빌드에 빠져 있는 경우가 많다. YouTube URL 재생은 mpv에 딸린 yt-dlp(구 youtube-dl) 훅을 통해 이루어지며 예: `mpv --vo=tct --ytdl-format="w" "url"`. — [mpv vo_tct.c 미러](https://git.tjdev.de/mirror/mpv/src/commit/e3618002e3f3441fc8543a93ea839f741f93f322/video/out/vo_tct.c) (검색 스니펫); [Arch forum](https://bbs.archlinux.org/viewtopic.php?id=285819) (검색 스니펫); [opensource.com 2018 글](https://opensource.com/article/18/12/linux-toy-youtube-dl) (검색 스니펫, 오래된 정보)
- tplay (maxcurzi/tplay): 이미지/영상을 ASCII로 렌더하는 Rust 미디어 플레이어. YouTube 재생은 선택적 의존성 yt-dlp 필요. — [tplay README](https://docs.rs/crate/tplay/0.9.3/source/README.md) (검색 스니펫)
- PKD667/asciitube: joelibaceta/video-to-ascii와 yt-dlp를 묶어 터미널에서 YouTube를 보는 자동화. — [github.com/PKD667/asciitube](https://github.com/PKD667/asciitube) (검색 스니펫)
- ascii-live (PyPI): YouTube URL 또는 로컬 파일을 ASCII로 재생. 프레임은 OpenCV, 스트림은 yt-dlp, 오디오는 Pygame. — [pypi.org/project/ascii-live](https://pypi.org/project/ascii-live/) (검색 스니펫)
- ascii-yt (PyPI): 터미널에서 YouTube 영상을 ASCII로 재생, 컬러 옵션. — [pypi.org/project/ascii-yt](https://pypi.org/project/ascii-yt/2.1.0) (검색 스니펫)
- mathiasvr/youtube-terminal: YouTube를 터미널 ASCII로 스트리밍(npm, FFmpeg 필요). 마지막 push가 2018년이라 현재 동작 여부 불확실. — [awesome.ecosyste.ms 항목](https://awesome.ecosyste.ms/projects/github.com%2Fmathiasvr%2Fyoutube-terminal) (검색 스니펫, 오래된 정보)
- console-cinema (kweonminsung): ASCII/픽셀 모드와 YouTube 검색 UI를 가진 Go 터미널 플레이어. — [awesome.ecosyste.ms 항목](https://awesome.ecosyste.ms/projects/github.com%2Fkweonminsung%2Fconsole-cinema) (검색 스니펫)
- ytsurf: 터미널에서 YouTube를 검색하고 썸네일 미리보기 후 mpv로 재생. — [ytsurf 노트](https://notes.nicolasdeville.com/github/ytsurf/) (검색 스니펫)
- ASCILINE: 브라우저 canvas에서 재생하지만 영상 소스는 서버 측 yt-dlp(480p 상한, video ID 캐시). 사용자가 직접 서버를 띄우는 셀프호스팅 도구. — [ASCILINE](https://github.com/YusufB5/ASCILINE) (열람)
- collidingScopes/ascii, video-stream-ascii 웹 데모 등 브라우저 전용 도구는 웹캠 또는 업로드 파일을 입력으로 받는다. — [awesome.ecosyste.ms 항목](https://awesome.ecosyste.ms/projects/github.com%2Fcollidingscopes%2Fascii), [video-stream-ascii-player](https://github.com/Im-Rises/video-stream-ascii-player) (검색 스니펫)
- 클라우드에서 호스팅되는 다운로더 서비스의 현황: public Cobalt API는 Turnstile CAPTCHA를 요구하게 되었고(`error.api.auth.turnstile.missing`), self-hosted Cobalt는 테스트 시점에 YouTube 처리에 실패했다는 2026-03 보고. — [dev.to, osovsky](https://dev.to/osovsky/i-was-building-a-cloud-video-service-youtube-turned-me-into-an-ip-trafficker-1l9o) (열람)

### Inferences
- 터미널 도구들이 YouTube를 "그냥 되는 것처럼" 지원할 수 있는 이유는 추출이 사용자의 가정용 IP에서, 사용자 한 명의 트래픽으로 일어나기 때문이다. 같은 yt-dlp 호출을 중앙 서버로 옮기면 IP 평판/레이트 리밋/PO 토큰 문제가 서비스 운영자에게 집중된다. 이것이 "호스팅 웹 서비스 + YouTube 링크" 조합의 선례가 드문 구조적 이유로 보인다.
- "Bad Apple" ASCII 플레이어류는 통상 저장소에 미리 변환한 프레임 데이터(또는 영상 파일)를 동봉하는 방식이라 소스 확보 문제가 없다(일반 지식이며 이번 조사에서 개별 저장소를 열람해 확인하지는 않음).
- 제품 관점의 기술적 결론: MVP는 "파일 업로드 + 완전 클라이언트 처리"가 가장 안전하고 서버 비용이 사실상 0이다. YouTube 링크는 (a) 사용자가 받은 파일을 업로드하도록 안내, (b) 데스크톱 Chromium 한정 탭 캡처 모드, (c) 브라우저 확장, (d) 서버 yt-dlp + residential 프록시 중에서 고르게 되며 (d)만이 "링크 붙여넣기만으로 동작"하는 UX를 주지만 운영 리스크와 [약관/법률 의존] 부담이 가장 크다.

### Gaps
- YouTube 링크를 받아 ASCII로 재생하는 "호스팅된 공개 웹 서비스"의 존재 여부를 확정하지 못했다. 검색에서 나오지 않았다는 것이지 없다고 확인한 것은 아니다.
- naughty-noob/yt2ascii, ASCIIPlayer(2025-03 itc.ua 보도) 등은 저장소 내용을 확인하지 못했다.
- ytfzf의 현재 유지보수 상태와 ASCII 출력 지원 방식은 조사하지 못했다.
- "Bad Apple" 웹 플레이어들의 개별 구현(프레임 데이터 포맷, 크기)은 열람하지 않았다.
