# YouTube 서비스 약관 및 API 정책이 "유튜브 링크 → 실시간 아스키 아트 + 오디오" 서비스에 가하는 제약 (2026년 11월 기준)

조사일: 2026-11-18. 1차 문서는 모두 이날 원문을 직접 내려받아 대조했다. 인용문은 원문 그대로이며 괄호 안이 한국어 풀이다.

문서별 기준일

| 문서 | 기준일 | URL |
|---|---|---|
| YouTube 서비스 약관 (한국 적용본, 영문/국문) | "Dated: January 5, 2022" / "발효일: 2022년 1월 5일" | https://www.youtube.com/t/terms?hl=ko&gl=KR |
| YouTube API Services Terms of Service | 본문에 발효일 없음. 페이지 "Last updated 2026-11-06 UTC". 개정 이력상 본문 최종 개정은 2022-07-12(4조) | https://developers.google.com/youtube/terms/api-services-terms-of-service |
| Developer Policies | 페이지 "Last updated 2026-11-06 UTC". 최근 개정 2026-06-01, 2026-05-04(파생 지표/데이터 보관 추가 정책) | https://developers.google.com/youtube/terms/developer-policies |
| Required Minimum Functionality (RMF) | 페이지 "Last updated 2026-11-06 UTC". 최근 개정 2025-07-07(임베드 플레이어 Referer 식별 의무 추가) | https://developers.google.com/youtube/terms/required-minimum-functionality |
| 개정 이력 | 최신 항목 2026-06-01 | https://developers.google.com/youtube/terms/revision-history |
| IFrame Player API 레퍼런스 | "Last updated 2026-10-15 UTC" | https://developers.google.com/youtube/iframe_api_reference |
| Data API 쿼터 문서 | "Last updated 2026-11-12 UTC" | https://developers.google.com/youtube/v3/determine_quota_cost |

---

## 1. YouTube 서비스 약관 "권한 및 제한사항"은 다운로드, 플레이어 외 접근, 변경/수정, 자동화 접근에 대해 무엇이라고 하는가

### Takeaway
약관은 "서비스가 명시적으로 승인한 방식"(재생, 임베드 플레이어) 외의 접근, 복제, 다운로드, 변경, 수정을 포괄적으로 금지하고, 복제 방지 기능 우회와 자동화 수단(스크래퍼) 접근도 별도로 금지한다. 서버가 유튜브 스트림을 가져와 아스키로 변환하는 설계는 1, 2, 3호에 동시에 걸린다. 다만 약관 본문에는 "오디오와 비디오를 분리"한다는 문구 자체는 없고, 그 문구는 API 개발자 정책(2번 질문)에 있다.

### Cited Findings
- 한국 적용본의 서비스 제공자는 Google LLC이며, 기준일은 2022년 1월 5일로 영문/국문이 같다. "The entity providing the Service is Google LLC, a company operating under the laws of Delaware" / "날짜: 2022년 1월 5일" — [YouTube ToS (EN, gl=KR)](https://www.youtube.com/t/terms?hl=en&gl=KR), [YouTube 서비스 약관 (KO)](https://www.youtube.com/t/terms?hl=ko&gl=KR)
- 허용 범위: "You may view or listen to Content for your personal, non-commercial use. You may also show YouTube videos through the embeddable YouTube player." (개인적, 비영리적 용도로 보고 들을 수 있고, 임베드 가능한 YouTube 플레이어로 동영상을 보여줄 수 있다.) 국문: "귀하는 개인적, 비영리적 용도로 콘텐츠를 보고 들을 수 있습니다. 귀하는 내장가능한 YouTube 플레이어를 통해 YouTube 동영상을 표시할 수도 있습니다." — [YouTube ToS](https://www.youtube.com/t/terms?hl=en&gl=KR)
- 제한 1호(다운로드, 변경, 수정): "access, reproduce, download, distribute, transmit, broadcast, display, sell, license, alter, modify or otherwise use any part of the Service or any Content except: (a) as expressly authorized by the Service; or (b) with prior written permission from YouTube and, if applicable, the respective rights holders;" 국문: "(a) 서비스의 명시적 승인, 또는 (b) YouTube 및 해당하는 경우 각 권리 소유자의 사전 서면 승인을 받은 경우를 제외하고는, 서비스나 콘텐츠의 어떤 부분에 대해서도 액세스, 복제, 다운로드, 배포, 전송, 방송, 표시, 판매, 라이선스 부여, 변경, 수정 또는 그 밖의 사용을 금지합니다." — [YouTube 서비스 약관](https://www.youtube.com/t/terms?hl=ko&gl=KR)
- 제한 2호(우회): "circumvent, disable, fraudulently engage with, or otherwise interfere with any part of the Service (or attempt to do any of these things), including security-related features or features that (a) prevent or restrict the copying or other use of Content or (b) limit the use of the Service or Content;" (콘텐츠 복사나 사용을 막거나 제한하는 기능을 포함해 서비스의 어떤 부분도 우회, 무력화, 방해하거나 시도해서는 안 된다.) — [YouTube ToS](https://www.youtube.com/t/terms?hl=en&gl=KR)
- 제한 3호(자동화 접근): "access the Service using any automated means (such as robots, botnets or scrapers) except (a) in the case of public search engines, in accordance with YouTube's robots.txt file; or (b) with YouTube's prior written permission;" 국문: "자동화된 수단(로봇, 봇넷 또는 스크래퍼 등)을 사용해 서비스에 액세스하면 안 됩니다." — [YouTube 서비스 약관](https://www.youtube.com/t/terms?hl=ko&gl=KR)
- 제한 9호(비개인적, 상업적 시청): "use the Service to view or listen to Content other than for personal, non-commercial use (for example, you may not publicly screen videos or stream music from the Service);" (개인적, 비영리적 용도 외의 목적으로 보거나 듣기 위해 서비스를 써서는 안 된다. 예: 공개 상영, 서비스에서 음악 스트리밍.) — [YouTube ToS](https://www.youtube.com/t/terms?hl=en&gl=KR)
- 제한 10호(광고 판매): "(b) sell advertising, sponsorships, or promotions on any page of any website or application that only contains Content from the Service or where Content from the Service is the primary basis for such sales (for example, selling ads on a webpage where YouTube videos are the main draw for users visiting the webpage)." (유튜브 콘텐츠만 있거나 유튜브 콘텐츠가 광고 판매의 주된 근거인 페이지에서 광고를 팔 수 없다.) — [YouTube ToS](https://www.youtube.com/t/terms?hl=en&gl=KR)
- 다른 이용자에게 주는 라이선스의 한계: "...to use that Content, including to reproduce, distribute, modify, display, and perform it, only as enabled by a feature of the Service (such as video playback or embeds). For clarity, this license does not grant any rights or permissions for a user to make use of your Content independent of the Service." (복제, 수정, 표시 등은 재생이나 임베드 같은 서비스 기능이 허용하는 범위에서만 가능하고, 서비스와 독립적으로 콘텐츠를 이용할 권리는 주지 않는다.) — [YouTube ToS](https://www.youtube.com/t/terms?hl=en&gl=KR)
- 준거법: 원칙은 캘리포니아주 법과 산타클라라 카운티 법원이지만, "If you reside in one of those countries, then where California law is excluded from applying, your country's laws will apply" (거주국 법원이 캘리포니아 법 적용을 배제하는 경우 거주국 법이 적용된다). 국문본에도 같은 조항이 있다. — [YouTube 서비스 약관](https://www.youtube.com/t/terms?hl=ko&gl=KR)
- 임베드 플레이어 이용에는 API 약관이 자동으로 따라붙는다: "The YouTube API Terms of Service and Developer Policies apply to all access and use of the YouTube embedded player." — [YouTube Help: Embed videos & playlists](https://support.google.com/youtube/answer/171780?hl=en)

### Inferences
- 한국 적용본과 글로벌본은 제한 조항 문구가 사실상 같다. 대조한 범위에서 한국본 고유 차이는 서비스 변경 시 사전 통지 문단 정도였고, 이번 주제와 관련된 금지 조항에는 차이가 없었다.
- 서버 측에서 영상 스트림을 받아 프레임을 아스키로 바꾸는 방식은 (1) 서비스가 승인하지 않은 접근/복제/수정, (2) 스트림 보호 기능 우회, (3) 자동화 접근에 모두 해당할 가능성이 높다. 약관상 예외는 "서비스가 명시적으로 승인"했거나 YouTube와 권리자의 사전 서면 허락이 있는 경우뿐이다.
- 영상 화면을 아스키로 대체해 보여주는 것은 콘텐츠의 "alter, modify"에 해당한다고 읽힐 여지가 크다. 다른 이용자 라이선스 조항도 "서비스 기능이 허용하는 범위"로 수정을 한정한다.

### Gaps
- 약관 본문에는 "separate/isolate audio and video"라는 표현이 없다. 약관만으로 오디오 단독 재생을 직접 금지하는 문장은 찾지 못했다(포괄 조항인 1호와 9호의 예시 "stream music"으로 포섭될 뿐이다).
- 한국 법원이 이 약관 조항들을 실제로 어떻게 해석했는지에 대한 판례는 조사하지 않았다(저작권법 담당 조사원 범위).

---

## 2. API 서비스 약관과 개발자 정책은 다운로드/캐시, 오디오·비디오 분리, 플레이어 변경/가림, 백그라운드 재생, 최소 크기, 광고/브랜딩, 상업적 이용에 대해 무엇이라고 하는가

### Takeaway
개발자 정책은 이 서비스의 핵심 동작을 거의 조항 단위로 금지한다. 시청각 콘텐츠의 다운로드/캐시/저장(III.E), 오디오·비디오 구성요소의 분리/격리/수정(III.I.7), 플레이어 기능의 수정/차단(III.I.6), 보이지 않는 플레이어 재생(III.I.9), 공식 API 외 기술로 콘텐츠 접근(III.I.14)이 모두 명시돼 있다. RMF는 플레이어 최소 200x200px, 플레이어 앞에 오버레이 금지, 절반 이상 보일 때만 자동재생을 요구한다.

### Cited Findings

API Services Terms of Service
- 계약 구성: API 약관, 개발자 정책, RMF, 브랜딩 가이드라인, YouTube 서비스 약관이 모두 "Agreement"에 포함된다. "YouTube Terms means the YouTube Terms of Service currently located at https://www.youtube.com/t/terms." — [API Services ToS](https://developers.google.com/youtube/terms/api-services-terms-of-service)
- 3.1 Compliance: "YouTube may suspend or terminate your access to, or use of, any aspect of the YouTube API Services (including any credentials assigned to you or your API Client(s)), impose additional requirements and restrictions, or terminate the Agreement between you and YouTube, for any violation of the Agreement" (위반 시 API 접근과 자격증명을 정지 또는 종료할 수 있다.) — [API Services ToS](https://developers.google.com/youtube/terms/api-services-terms-of-service)
- 6 API Clients and Monitoring: "YouTube may monitor, review and inspect your API Client(s), and monitor and audit your access to and use of the YouTube API Services, at any time and without further notice to you" (사전 통지 없이 언제든 점검, 감사할 수 있다.) — [API Services ToS](https://developers.google.com/youtube/terms/api-services-terms-of-service)
- 15 Usage and Quotas: "You and your API Client(s) will not, and will not attempt to, exceed or circumvent use or quota restrictions." (쿼터 초과나 우회 금지.) — [API Services ToS](https://developers.google.com/youtube/terms/api-services-terms-of-service)
- 16.3: "no rights or licenses are granted to reproduce or distribute audiovisual content or make audiovisual content available in any manner other than through the use of the YouTube API Services in accordance with the Agreement." (계약에 따른 API 이용 외의 방식으로 시청각 콘텐츠를 복제, 배포, 제공할 권리는 부여되지 않는다.) — [API Services ToS](https://developers.google.com/youtube/terms/api-services-terms-of-service)
- 24.2 Termination by YouTube: "Although we will try to give you reasonable notice, we have no obligation to do so." (합리적 통지를 하려 하겠지만 의무는 없다.) — [API Services ToS](https://developers.google.com/youtube/terms/api-services-terms-of-service)

Developer Policies (섹션 III)
- III.E "Audiovisual Content": "You and your API Clients must not, and must not encourage, enable, or require others to: download, import, backup, cache, or store copies of YouTube audiovisual content without YouTube's prior written approval, make content available for offline playback, or use any aspect of the YouTube API Services to facilitate or promote copyright infringement" (YouTube의 사전 서면 승인 없이 시청각 콘텐츠를 다운로드, 가져오기, 백업, 캐시, 저장해서는 안 되고, 오프라인 재생을 제공해서도 안 된다.) — [Developer Policies](https://developers.google.com/youtube/terms/developer-policies)
- III.E 스크래핑: "You and your API Clients must not, and must not encourage, enable, or require others to, directly or indirectly, scrape YouTube Applications or Google Applications, or obtain scraped YouTube data or content." (직간접 스크래핑과 스크래핑된 데이터 취득 금지.) — [Developer Policies](https://developers.google.com/youtube/terms/developer-policies)
- III.I.4: "modify, interfere with, replace, or otherwise disable any functionality, data, or content made available as part of, or in connection with, YouTube API Services. For example, you must not remove, obscure, alter, or disable any links that appear in YouTube players or in API Data." (API로 제공되는 기능, 데이터, 콘텐츠를 수정, 방해, 대체, 비활성화 금지.) — [Developer Policies](https://developers.google.com/youtube/terms/developer-policies)
- III.I.5: "modify, interfere with, replace, or block advertisements placed or served by YouTube or by YouTube API Services including in API Data, YouTube audiovisual content, or YouTube players;" (YouTube 광고의 수정, 방해, 대체, 차단 금지.) — [Developer Policies](https://developers.google.com/youtube/terms/developer-policies)
- III.I.6: "modify, build upon, or block any portion or functionality of a YouTube player;" (YouTube 플레이어의 어떤 부분이나 기능도 수정, 그 위에 구축, 차단 금지.) — [Developer Policies](https://developers.google.com/youtube/terms/developer-policies)
- III.I.7: "separate, isolate, or modify the audio or video components of any YouTube audiovisual content made available as part of, or in connection with, YouTube API Services. For example, you must not apply alternate audio tracks to videos;" (시청각 콘텐츠의 오디오 또는 비디오 구성요소를 분리, 격리, 수정 금지. 예: 영상에 다른 오디오 트랙 입히기.) — [Developer Policies](https://developers.google.com/youtube/terms/developer-policies)
- III.I.8: "promote separately the audio or video components of any YouTube audiovisual content made available as part of, or in connection with, the YouTube API Services;" (오디오나 비디오 구성요소를 따로 홍보 금지.) — [Developer Policies](https://developers.google.com/youtube/terms/developer-policies)
- III.I.9: "create, include, or promote features that play content, including audio or video components, from a background player, meaning a player that is not displayed in the page, tab, or screen that the user is viewing;" (사용자가 보고 있는 페이지, 탭, 화면에 표시되지 않는 "백그라운드 플레이어"에서 콘텐츠를 재생하는 기능 금지.) — [Developer Policies](https://developers.google.com/youtube/terms/developer-policies)
- III.I.14: "use any technology other than YouTube API Services to access or retrieve API Data, including to access any portion of any YouTube audiovisual content;" (YouTube API 서비스 외의 기술로 시청각 콘텐츠의 어떤 부분에도 접근 금지.) — [Developer Policies](https://developers.google.com/youtube/terms/developer-policies)
- III.I.1: "API Clients must not mimic or replicate YouTube's core user experiences by recreating features or process flows unless they add significant independent value or functionality that improves users' interactions with YouTube." (독립적 가치를 크게 더하지 않는 한 YouTube 핵심 경험 복제 금지.) — [Developer Policies](https://developers.google.com/youtube/terms/developer-policies)
- III.I.21 (2022-06-02 추가): "situate the YouTube player in a nested or hierarchical iframe lineage to circumvent YouTube policies or otherwise obfuscate the source of use." (정책 회피나 출처 은폐 목적의 중첩 iframe 금지.) — [Developer Policies](https://developers.google.com/youtube/terms/developer-policies), [Revision History](https://developers.google.com/youtube/terms/revision-history)
- III.F 브랜딩/출처 표시: "Any API Client page or feature that displays YouTube content ... must make clear to the viewer that YouTube is the source of the relevant content" 및 "must not ... interfere with or obscure any attribution provided by YouTube, including attribution provided via or shown in embedded YouTube players." (YouTube가 출처임을 분명히 하고, 플레이어 안의 출처 표시를 가리지 말 것.) — [Developer Policies](https://developers.google.com/youtube/terms/developer-policies)
- III.F 재생 무결성: "API Clients must not charge users to watch content in an embedded YouTube player." 및 "API Clients must not otherwise gate access to a video by requiring a user to take an action other than clicking the play button" (임베드 플레이어 시청에 요금 부과 금지, 재생 버튼 외 행동 요구 금지.) — [Developer Policies](https://developers.google.com/youtube/terms/developer-policies)
- III.G.1 금지: "sell advertising, sponsorships, or promotions that are placed on or within YouTube audiovisual content or the YouTube player without YouTube's prior written approval" 및 III.G.1.d "sell advertising, sponsorships, or promotions on any page or screen that contains YouTube API Data unless other data, content, or material not obtained from YouTube appears on the same page and offers enough independent value to justify such sales if the YouTube API Data were removed." (YouTube 데이터가 없어도 광고 판매를 정당화할 독립적 가치가 같은 페이지에 있어야 한다.) — [Developer Policies](https://developers.google.com/youtube/terms/developer-policies)
- III.G.2 허용: "Developing ad-enabled API Clients, such as an ad-enabled blog or website, that use YouTube API Services subject to compliance with all other terms of the Agreement, including the restrictions in section III.G.1.d" 및 "Selling an API Client" (광고가 붙은 클라이언트 개발, 클라이언트 판매는 조건부 허용.) — [Developer Policies](https://developers.google.com/youtube/terms/developer-policies)
- III.H 감사: YouTube가 요청하면 정해진 기한 안에 "provide YouTube with account(s) necessary to access all features or functions of the current, in-production version(s) of your API Clients" 해야 하고, "YouTube may use any technical means to overcome non-compliance with these provisions." (비준수 극복을 위해 어떤 기술적 수단도 쓸 수 있다.) — [Developer Policies](https://developers.google.com/youtube/terms/developer-policies)

Required Minimum Functionality
- 플레이어 크기: "Embedded players must have a viewport that is at least 200px by 200px. If the player displays controls, it must be large enough to fully display the controls without shrinking the viewport below the minimum size. We recommend 16:9 players be at least 480 pixels wide and 270 pixels tall." (뷰포트 최소 200x200px, 16:9는 480x270 이상 권장.) — [RMF](https://developers.google.com/youtube/terms/required-minimum-functionality)
- 오버레이: "You must not display overlays, frames, or other visual elements in front of any part of a YouTube embedded player, including player controls. Similarly, you must not use overlays, frames or other visual elements to obscure any part of an embedded player, including player controls." (플레이어의 어느 부분 앞에도 오버레이, 프레임, 시각 요소를 두거나 가려서는 안 된다.) — [RMF](https://developers.google.com/youtube/terms/required-minimum-functionality)
- 자동재생: "an API Client must not initiate an automatic playback until the player is visible and more than half of the player is visible on the page or screen." 및 "A page or screen must not have more than one YouTube player that automatically plays content simultaneously." (플레이어가 절반 넘게 보이기 전에는 자동재생 금지, 한 화면에 자동재생 플레이어 둘 이상 금지.) — [RMF](https://developers.google.com/youtube/terms/required-minimum-functionality)
- 플레이어 속성: "You must not make changes to the YouTube player that are not explicitly described by the API documentation." (API 문서가 명시하지 않은 플레이어 변경 금지.) — [RMF](https://developers.google.com/youtube/terms/required-minimum-functionality)
- 식별(2025-07-07 추가): "API Clients that use the YouTube embedded player (including the YouTube IFrame Player API) must provide identification through the HTTP Referer request header." 및 "Failure to comply with these requirements might result in reduced functionality in the YouTube embedded player." (Referer로 신원을 밝혀야 하며, 미준수 시 플레이어 기능이 제한될 수 있다.) — [RMF](https://developers.google.com/youtube/terms/required-minimum-functionality), [Revision History](https://developers.google.com/youtube/terms/revision-history)

### Inferences
- 임베드 플레이어를 0px, 화면 밖, `display:none`, 불투명도 0으로 숨기고 오디오만 쓰는 설계는 III.I.9(백그라운드 플레이어), RMF 최소 크기, RMF 오버레이 조항을 동시에 위반한다. 플레이어 위에 아스키 캔버스를 겹쳐 올리는 설계도 오버레이 조항에 정면으로 걸린다.
- "영상 화면 대신 아스키를 보여주고 오디오만 원본"이라는 제품 정의 자체가 III.I.7 "separate, isolate, or modify the audio or video components"의 문언에 해당한다. 예시로 든 "alternate audio tracks"의 반대 방향(영상 교체)이지만 조문은 양쪽을 모두 포괄한다.
- 상업적 운영 자체는 금지되지 않는다. 다만 광고를 붙이려면 유튜브 콘텐츠 없이도 성립하는 독립적 가치가 페이지에 있어야 하고(III.G.1.d), 시청에 요금을 받을 수는 없다(III.F).
- 개발자 정책의 세부 번호 가운데 III.I.1~21과 III.G.1.d는 원문과 개정 이력으로 번호를 확인했다. "Audiovisual Content"와 스크래핑 조항은 섹션 III.E 안에 있으나 하위 번호(예: E.1, E.6)는 페이지 구조에서 읽은 것으로 별도 확인하지 않았다.

### Gaps
- "prior written approval"(사전 서면 승인) 신청이 이런 변환형 시각화 서비스에 실제로 승인된 사례가 있는지 공개 자료를 찾지 못했다.
- 플레이어 "옆"에 두는 콘텐츠의 허용 범위를 직접 규정한 조항은 없다. 금지 조항들의 반대해석에 의존해야 한다(3번 질문 참고).

---

## 3. IFrame Player API는 실제로 무엇을 노출하는가. 프레임/픽셀/원시 스트림을 주는가. 숨긴 플레이어는 허용되는가. 준수형 설계는 가능한가

### Takeaway
IFrame Player API는 재생 제어와 상태 조회(시간, 길이, 볼륨, 속도, 상태 이벤트, 자막 옵션)만 제공하고, 프레임, 픽셀, 오디오 샘플, 미디어 스트림 URL은 전혀 제공하지 않는다. 따라서 공식 API만으로는 유튜브 영상의 화면에서 아스키를 만들 수 없다. 준수형 설계는 "공식 플레이어를 200x200px 이상으로 가리지 않고 보여주고, 그 옆에 유튜브 영상 픽셀에서 파생되지 않은 것을 표시"하는 형태로 한정된다.

### Cited Findings
- 문서화된 함수: 큐/로드(`cueVideoById`, `loadVideoById`, `cuePlaylist`, `loadPlaylist` 등), 재생(`playVideo`, `pauseVideo`, `stopVideo`, `seekTo`), 볼륨(`mute`, `unMute`, `isMuted`, `setVolume`, `getVolume`), 크기(`setSize`), 속도(`getPlaybackRate`, `setPlaybackRate`, `getAvailablePlaybackRates`), 상태(`getPlayerState`, `getCurrentTime`, `getDuration`, `getVideoLoadedFraction`), 정보(`getVideoUrl`, `getVideoEmbedCode`), 360도(`getSphericalProperties`, `setSphericalProperties`), 모듈(`getOptions`, `getOption`, `setOption`), DOM(`getIframe`, `destroy`). — [IFrame Player API Reference](https://developers.google.com/youtube/iframe_api_reference)
- 이벤트: `onReady`, `onStateChange`, `onPlaybackQualityChange`, `onPlaybackRateChange`, `onError`, `onApiChange`, `onAutoplayBlocked`. — [IFrame Player API Reference](https://developers.google.com/youtube/iframe_api_reference)
- 화질: 2026-10-15 판 레퍼런스에는 화질 조회/설정 함수(`setPlaybackQuality`, `getPlaybackQuality`, `getAvailableQualityLevels`)가 없다(원문 전체 검색에서 미검출). 화질은 `onPlaybackQualityChange` 이벤트로만 통지된다. — [IFrame Player API Reference](https://developers.google.com/youtube/iframe_api_reference)
- 자막: "Currently, the only module that you can set options for is the captions module" (옵션을 설정할 수 있는 모듈은 captions뿐). 문서화된 옵션은 글자 크기와 reload이며, 자막 텍스트를 읽는 함수는 없다. — [IFrame Player API Reference](https://developers.google.com/youtube/iframe_api_reference)
- 프레임, 픽셀, 캔버스, 원시 오디오, 미디어 스트림에 접근하는 함수나 이벤트는 레퍼런스에 없다. `getIframe()`은 임베드된 `<iframe>` DOM 노드를 돌려줄 뿐이다. — [IFrame Player API Reference](https://developers.google.com/youtube/iframe_api_reference)
- 최소 크기 요구가 API 레퍼런스 본문에도 그대로 있다: "Embedded players must have a viewport that is at least 200px by 200px." — [IFrame Player API Reference](https://developers.google.com/youtube/iframe_api_reference)
- 플레이어 파라미터: `autoplay`, `cc_lang_pref`, `cc_load_policy`, `color`, `controls`, `disablekb`, `enablejsapi`, `end`, `fs`, `hl`, `iv_load_policy`, `list`, `listType`, `loop`, `origin`, `playlist`, `playsinline`, `rel`, `start`, `widget_referrer`. `modestbranding`은 "deprecated and has no effect"(폐기되어 효과 없음)이며 `showinfo`, `autohide`, `theme`도 폐기됐다. — [Player Parameters](https://developers.google.com/youtube/player_parameters)
- 2025년 하반기 이후 Referer를 보내지 않는 임베드는 "Error 153: Video player configuration error"로 재생이 막히는 사례가 다수 보고됐다(Django 기본 Referrer-Policy, Safari, 크롬 확장 페이지 등). — [Simon Willison, 2025-12-01](https://simonwillison.net/2025/Dec/1/youtube-embed-153-error/), [Chromium Extensions 그룹](https://groups.google.com/a/chromium.org/g/chromium-extensions/c/OUJad0q-d_g)

### Inferences
- 유튜브 iframe은 교차 출처이므로 부모 페이지의 자바스크립트가 `<video>` 요소에 접근하거나 캔버스로 그릴 수 없다. 이것은 브라우저 동일 출처 정책에서 나오는 결론으로, API 문서에 명시된 문장은 아니다.
- 화면 캡처 API(`getDisplayMedia`)로 사용자가 직접 탭을 공유하게 해 플레이어 픽셀을 읽는 방식은 기술적으로 가능할 수 있으나, III.I.7(비디오 구성요소 수정), III.I.14(API 외 기술로 시청각 콘텐츠 접근), 약관 1호(변경, 수정)에 해당한다는 해석이 자연스럽다. 이를 허용하거나 금지한다고 직접 밝힌 YouTube 공식 문서는 찾지 못했으므로 추론이다.
- 문언상 허용되는 "플레이어 옆의 무언가"의 조건: (a) 플레이어를 가리지 않고, (b) 플레이어가 200x200px 이상으로 사용자가 보는 화면에 실제 표시되며, (c) 유튜브 시청각 콘텐츠의 픽셀이나 오디오 샘플에서 파생되지 않고, (d) 광고 등 플레이어 기능을 막지 않을 것. 예컨대 `getCurrentTime()`과 `onStateChange`로 동기화한 자체 제작 애니메이션, 가사나 주석, 사용자가 권리를 가진 별도 영상 파일에서 만든 아스키 렌더링은 조문과 충돌하지 않는다. 반면 "유튜브 영상 그 자체의 아스키 버전"은 공식 경로로 픽셀을 얻을 방법이 없어 이 범주에 들어가지 못한다.
- 플레이어를 보이게 두더라도 페이지의 주된 시각 요소가 아스키이고 플레이어는 구석의 200x200 상자라면, III.I.8(오디오 구성요소를 따로 홍보)이나 III.I.9의 취지에 어긋난다는 지적을 받을 위험이 있다. 이것은 조문 해석상 위험 평가이며 YouTube의 공식 판단 사례는 확인하지 못했다.

### Gaps
- 화질 관련 함수가 레퍼런스에서 언제 삭제됐는지는 IFrame API 개정 이력 페이지를 따로 확인하지 않아 특정하지 못했다.
- 화면 캡처 기반 재렌더링에 대한 YouTube의 공식 입장이나 집행 사례는 찾지 못했다.
- Error 153과 Referer 요구의 연결은 커뮤니티 보고와 RMF 문구("reduced functionality")를 맞춘 것으로, YouTube가 오류 코드 153을 직접 설명한 공식 문서는 확인하지 못했다.

---

## 4. YouTube Data API v3: 쿼터, 제공 메타데이터, 스트림/다운로드 URL 제공 여부, 스트림 접근 공식 프로그램

### Takeaway
Data API v3는 메타데이터와 임베드 HTML만 주고, 어떤 공식 API도 타인 영상의 미디어 스트림이나 다운로드 URL을 주지 않는다. 기본 쿼터는 2026년 11월 현재 "search.list 100회, videos.insert 100회, 그 밖의 엔드포인트 합산 하루 10,000단위"로 문서화돼 있다. 스트림에 준하는 접근은 본인 업로드 영상의 다운로드(Studio, Takeout)뿐이고, Player for Education은 스트림 접근이 아니라 유료 라이선스형 임베드 플레이어다.

### Cited Findings
- 기본 쿼터: "Projects that enable the YouTube Data API have a default quota allocation of 100 search.list calls, 100 videos.insert calls, and 10,000 units per day combined for all other endpoints." 및 "The search.list and videos.insert methods have their own quota buckets." (search.list와 videos.insert는 별도 버킷으로 각각 하루 100회, 나머지는 합산 하루 10,000단위.) — [Quota Calculator](https://developers.google.com/youtube/v3/determine_quota_cost), [Getting Started](https://developers.google.com/youtube/v3/getting-started)
- 비용 예: 대부분의 `list` 호출 1단위(`videos.list`, `playlistItems.list`), 대부분의 쓰기 50단위, `captions.list` 50단위, `captions.insert` 400단위. — [Quota Calculator](https://developers.google.com/youtube/v3/determine_quota_cost)
- 쿼터 증액은 감사를 거쳐야 한다: "If you would like to request additional quota beyond the default allocation, you must first complete an audit to show that your project is in compliance" 취지. 정기 감사(Periodic audit)와 감사 불합격 이의 절차도 같은 페이지에 있다. — [Quota and Compliance Audits](https://developers.google.com/youtube/v3/guides/quota_and_compliance_audits)
- 정책 원문: "you can apply for a quota extension by completing an API Compliance Audit where you must specify the use case for which you need the extension." 및 "If YouTube approves the application, you must use the additional quota granted only for the approved use case." — [Developer Policies III.D](https://developers.google.com/youtube/terms/developer-policies)
- 비활성 프로젝트: "YouTube reserves the right to disable or curtail your access to, or use of, specific YouTube API Services if your API Project has been inactive for 90 consecutive days. For example, YouTube could revoke your API Credentials, or reduce (or eliminate) your API Project's quotas" (90일 연속 비활성 시 자격증명 회수나 쿼터 축소 가능.) — [Developer Policies III.D](https://developers.google.com/youtube/terms/developer-policies)
- `videos` 리소스가 주는 것: snippet(제목, 설명, 썸네일 등), contentDetails(길이, 자막 유무, `licensedContent`), status(`license` 값 `youtube` 또는 `creativeCommon`, `embeddable`), statistics, `player.embedHtml`(임베드용 iframe HTML). 리소스에 스트림 URL이나 다운로드 URL 필드는 없다. — [Videos resource](https://developers.google.com/youtube/v3/docs/videos)
- `fileDetails`(업로드 원본의 코덱, 해상도, 비트레이트 등 정보)는 소유자 전용이다: "This data can only be retrieved by the video owner." 파일 자체가 아니라 파일에 대한 메타데이터다. — [Videos resource](https://developers.google.com/youtube/v3/docs/videos)
- 자막 다운로드: `captions.download`는 200단위이며 "This method requires the user to have permission to edit the video." (영상 편집 권한이 있는 사용자만 가능.) — [Captions: download](https://developers.google.com/youtube/v3/docs/captions/download)
- API 데이터 보관: 비인가 데이터는 30일 뒤 삭제하거나 새로 고쳐야 한다("After 30 calendar days, the API Client must either delete or refresh the stored data" 취지). 2026-05-04와 06-01 개정으로 감사를 통과하고 별도 신청한 분석 용도에 한해 30일 초과 통계 보관이 허용됐다. — [Developer Policies III.E.4](https://developers.google.com/youtube/terms/developer-policies), [Revision History](https://developers.google.com/youtube/terms/revision-history)
- 본인 영상 다운로드: "You can download MP4 files of YouTube videos that you've uploaded to YouTube in either 720p or 360p, depending on the video size. You can also use Google Takeout to download all the videos you've uploaded." 하루에 영상당 5회 제한. 같은 페이지에 "Note: You can't download other user's YouTube videos." (타인의 영상은 다운로드할 수 없다.) — [YouTube Help: Download YouTube videos that you've uploaded](https://support.google.com/youtube/answer/56100?hl=en)
- Player for Education: "Our educational partners pay to license the Player for Education from YouTube. ... the player doesn't show ads." (교육 파트너가 YouTube에 라이선스 비용을 내고 쓰는 광고 없는 임베드 플레이어.) 창작자는 임베드를 켜 둔 영상이 대상이 되며 시청 시간 비율로 수익을 받는다. 도메인은 youtubeeducation.com. — [YouTube Help: Earn with Player for Education](https://support.google.com/youtube/answer/15503014?hl=en)
- Player for Education은 Canvas, EdPuzzle, Seesaw 같은 교육 플랫폼과 LMS 통합용으로 소개됐다. — [YouTube Blog](https://blog.youtube/inside-youtube/youtube-player-education-classroom-learning/)

### Inferences
- "링크만 넣으면 아무 영상이나"라는 기능에 필요한 원시 미디어를 주는 공식 경로는 없다. 채널 소유자가 자기 영상 파일을 Studio나 Takeout으로 내려받아 서비스에 직접 업로드하는 흐름만이 YouTube 계약과 충돌하지 않는 미디어 확보 경로다(이 경우 유튜브 링크가 아니라 파일 업로드 서비스가 된다).
- 메타데이터 조회만 한다면 `videos.list` 1단위로 하루 약 10,000회가 가능하지만, 검색 기능을 붙이면 하루 100회 버킷이 곧바로 병목이 된다.
- Player for Education은 여전히 YouTube가 렌더링하는 플레이어이므로 프레임이나 스트림 접근 수단이 아니다. 아스키 변환 용도에는 도움이 되지 않는다.

### Gaps
- Player for Education의 파트너 자격 요건, 요금, 신청 절차에 관한 공식 공개 문서를 찾지 못했다. `developers.google.com/youtube/player-for-education` 주소는 내용이 없는 페이지였다.
- 콘텐츠 파트너(CMS, Content ID 보유자)에게 스트림이나 원본 파일 접근을 주는 별도 계약이 있는지는 공개 문서로 확인하지 못했다.
- 쿼터의 별도 버킷 구조(search.list/videos.insert 각 100회)가 언제 도입됐는지는 확인하지 못했다. 이전에는 search.list가 100단위였으므로 최근 변경으로 보이지만 개정 일자는 찾지 못했다.

---

## 5. 집행 이력: YouTube/Google과 권리자 단체는 다운로드, 재렌더링 도구에 무엇을 해 왔는가. 위반 API 프로젝트는 어떻게 되는가

### Takeaway
집행은 세 갈래로 진행돼 왔다. YouTube/Google의 직접 조치는 대부분 약관 위반을 근거로 한 중지 요구 서한(Groovy, Rythm 2021, Vanced 2022, Invidious 2023)이었고, 소송과 DMCA 조치는 주로 음반 업계(RIAA)가 맡았으며, 2024년 이후에는 PO 토큰, SABR, 자바스크립트 챌린지 같은 기술적 차단이 중심이 됐다. 아스키 재렌더링 서비스를 직접 겨냥한 조치 사례는 찾지 못했다.

### Cited Findings

YouTube/Google의 직접 조치
- Groovy(디스코드 음악 봇): Google이 중지 요구 서한을 보내 7일 내 준수를 요구했고 2021-08-30 종료했다. Google은 The Verge에 "We notified Groovy about violations of our Terms of Service"라고 밝히며 서비스 변경과 상업적 이용을 위반 사유로 들었다. — [9to5Google, 2021-08-25](https://9to5google.com/2021/08/25/youtube-nukes-popular-groovy-bot-discord-music-service-for-breaking-platforms-tos/)
- Rythm: 같은 방식의 서한(7일 기한)을 받고 2021-09-15 종료. — [NME](https://www.nme.com/news/discord-music-bot-rythm-follows-groovy-into-the-void-after-cease-and-desist-3045407)
- Vanced: "Google sent the Vanced owners a cease and desist letter recently, which has forced the developers to stop distributing and developing the app." 개발진 설명은 "We were asked to remove all references to 'YouTube', change the logo, and remove all links related to YouTube products". 2022년 3월 종료. — [The Verge, 2022-03-13](https://www.theverge.com/2022/3/13/22975890/youtube-vanced-app-discontinued-shut-down-legal-reasons-google)
- Invidious: 2023-06-08 YouTube 법무팀이 API 약관과 개발자 정책 위반을 이유로 서한을 보냈다. "We hope that you will cooperate with us by correcting and ceasing to Offer Your Client that violates our terms and policies within 7 days from the date of this letter". 개발진은 "we never agreed to any of their TOS/policies ... we don't use their API"라며 거부했다. — [TorrentFreak, 2023-06-09](https://torrentfreak.com/youtube-orders-invidious-privacy-software-to-shut-down-in-7-days-230609/)
- Invidious 서한 이후 소송이나 공식 후속 조치는 보도되지 않았다. — [Vice](https://www.vice.com/en/article/youtube-tells-open-source-privacy-software-invidious-to-shut-down)

권리자 단체(RIAA, 음반사)의 조치
- youtube-dl: RIAA가 2020-10-23 DMCA 1201조(기술적 보호조치 우회)를 근거로 GitHub에 삭제를 요구해 저장소가 내려갔다. EFF가 "Youtube-dl stands in place of a web browser and performs a similar function with respect to user-uploaded videos"라는 취지의 서한을 보낸 뒤 GitHub이 2020-11-16 복원했다. GitHub은 1201조 요청을 전문가가 검토하도록 절차를 바꾸고 100만 달러 개발자 방어 기금을 만들었다. — [EFF](https://www.eff.org/deeplinks/2020/11/github-reinstates-youtube-dl-after-riaas-abuse-dmca), [The Register](https://www.theregister.com/2020/11/16/github_restores_youtubedl/)
- FLVTO.biz, 2conv.com: 음반사들이 2018년 제소. 2019년 1월 관할 없음으로 기각됐으나 제4연방항소법원이 뒤집었다. 운영자가 소송 참여를 중단해 궐석 판결이 났고, 2022년 2월 버지니아 연방법원이 약 8,300만 달러(저작물 1,618건에 건당 5만 달러 기준, 권고액 82,922,500달러) 배상을 명했다. 운영자는 자금 부족으로 항소를 포기하고 미국 접속을 차단했다. — [Music Business Worldwide](https://www.musicbusinessworldwide.com/labels-awarded-83m-in-lawsuit-against-operator-of-stream-ripping-sites123456/), [Complete Music Update](https://archive.completemusicupdate.com/article/us-judge-recommends-that-the-majors-should-get-82922500-in-damages-from-stream-ripping-sites/)
- Yout v. RIAA: 스트림 리핑 사이트 Yout이 RIAA의 구글 검색 삭제 요청에 맞서 확인 소송을 냈으나, 코네티컷 연방지방법원(Underhill 판사)이 2022년 가을 RIAA 승소로 기각했다. 법원은 Yout이 YouTube의 기술적 보호조치를 우회하지 않는다는 점을 보이지 못했다고 봤다. 제2연방항소법원 항소(No. 22-2760)는 2026년 4월 보도 시점에 "has been pending for a while"로 계류 중이었고, 2026년 3월에도 Cox 판결 관련 보충 서면이 오갔다. — [TorrentFreak, 2026-04-03](https://torrentfreak.com/yout-com-hopes-supreme-courts-cox-ruling-helps-its-case-riaa-disagrees/), [CourtListener 서면](https://storage.courtlistener.com/recap/gov.uscourts.ca2.59200/gov.uscourts.ca2.59200.146.0.pdf)
- AI 음악 업체 Suno와 Udio가 이 항소에 의견서를 냈다. YouTube의 보호조치가 접근 통제로 인정되면 자신들의 공정이용 항변이 약해진다는 우려 때문이다. — [TorrentFreak, 2025-10-08](https://torrentfreak.com/suno-udio-wade-into-youtube-ripper-circumvention-lawsuit-appeal-251008/)

2024~2026년 기술적 차단
- yt-dlp는 2025-11-12 릴리스부터 YouTube 지원에 외부 자바스크립트 런타임(Deno 권장, Node, QuickJS, Bun 지원)을 요구한다. YouTube의 자바스크립트 챌린지가 내장 해석기로 감당할 수 없게 복잡해졌기 때문이며, 런타임이 없으면 받을 수 있는 포맷이 제한된다. — [yt-dlp 공지 이슈 #15012](https://github.com/yt-dlp/yt-dlp/issues/15012), [Gigazine, 2025-11-13](https://www.gigazine.net/gsc_news/en/20251113-yt-dlp-required-deno-javascript-runtime)
- 2024년 중반 무렵부터 대부분의 포맷 요청에 BotGuard가 서명한 PO(Proof of Origin) 토큰이 요구되기 시작했고, 일부 클라이언트에는 SABR 스트리밍이 강제되고 있다는 보고가 이어진다. — [PiunikaWeb, 2025-09-25](https://piunikaweb.com/2025/09/25/youtube-token-checks-third-party-issues/), [yt-dlp 이슈 #16747](https://github.com/yt-dlp/yt-dlp/issues/16747)
- 2026년 1월에는 광고 차단기 사용자에게 "Content Unavailable"이 표시되고 다운로더 차단이 강화됐다는 보도가 있었다. — [PiunikaWeb, 2026-01-30](https://piunikaweb.com/2026/01/30/youtube-blocking-video-downloaders-premium-crackdown/)

API 프로젝트 위반 시 절차(계약상)
- 위반 시 YouTube는 접근과 자격증명을 정지 또는 종료할 수 있고(API ToS 3.1, 24.2), 통지 의무는 없다. — [API Services ToS](https://developers.google.com/youtube/terms/api-services-terms-of-service)
- 쿼터 증액에는 API Compliance Audit이 필수이며, 정기 감사도 실시된다. 감사 불합격에 대한 이의 절차가 있다. — [Quota and Compliance Audits](https://developers.google.com/youtube/v3/guides/quota_and_compliance_audits)

### Inferences
- YouTube가 직접 보낸 서한은 모두 저작권이 아니라 약관/API 정책 위반을 근거로 했고, 7일 기한이라는 형식이 반복된다(Groovy, Rythm, Invidious). 규모가 크고 광고를 우회하거나 오디오만 뽑아 쓰는 서비스가 표적이 됐다는 점에서, 오디오만 원본으로 들려주는 아스키 서비스는 Groovy/Rythm 유형과 구조가 가장 가깝다.
- Invidious 사례는 "API를 쓰지 않았으니 API 약관에 동의한 적 없다"는 항변으로 서한을 무시해도 소송까지 가지 않은 선례지만, 이후 YouTube는 법적 조치 대신 기술적 차단으로 대응 수단을 옮겼다. 서버에서 스트림을 가져오는 서비스는 법적 위험과 별개로 PO 토큰, SABR, 챌린지 변경 때문에 상시 깨질 운영 위험을 진다.
- 스트림 리핑 사이트에 대한 손해배상 판결과 Yout 1심은 YouTube 스트림 추출을 미국 DMCA 1201조의 우회로 본 방향이다. 다만 항소심이 계류 중이어서 확정된 법리는 아니다.

### Gaps
- 정책 위반을 이유로 특정 API 키나 프로젝트가 회수된 구체적 사례(날짜, 대상, YouTube의 설명)는 신뢰할 만한 출처로 확인하지 못했다. 계약상 권한이 있다는 점만 확인됐다.
- YouTube/Google이 스트림 리핑 사이트를 직접 제소한 사례는 찾지 못했다. 확인된 소송은 모두 음반사 또는 RIAA가 원고다.
- youtube-mp3.org 사건(2016년 제소, 2017년 종료)은 검색 결과에서 지나가는 언급만 확인했고 합의 조건을 1차 자료로 검증하지 못했다.
- NewPipe, ReVanced 등 다른 서드파티 클라이언트에 대한 2024~2026년 법적 조치는 찾지 못했다. Yout 항소심 판결이 2026년 4월 이후 선고됐는지도 확인하지 못했다(검색에서 판결문 미발견).
- 2024~2026년 기술적 차단에 대한 YouTube의 공식 발표문은 찾지 못했다. 관련 근거는 yt-dlp 저장소와 2차 보도다.
- 아스키, 필터, 시각화처럼 영상을 재렌더링하는 서비스를 직접 겨냥한 집행 사례는 찾지 못했다.

---

## 6. 크리에이티브 커먼즈 영상이나 채널 소유자 본인 영상에 대한 특칙이 YouTube 플랫폼 안에서의 허용 범위를 바꾸는가

### Takeaway
CC BY 표시는 저작권 측면의 재사용 허락일 뿐, YouTube 약관이나 API 정책의 다운로드, 분리, 수정 금지를 풀어주는 예외 조항은 없다. 계약상 차이가 생기는 것은 본인이 올린 영상뿐이며, 그것도 YouTube Studio나 Takeout으로 파일을 내려받는 공식 기능을 통해서다.

### Cited Findings
- 라이선스 유형은 두 가지다: "The standard YouTube license is the default setting for all YouTube uploads" 와 "Creative Commons Attribution license". — [YouTube Help: License types](https://support.google.com/youtube/answer/2797468?hl=en)
- CC BY의 의미: "If you add a Creative Commons Attribution license to your video, it means other creators can reuse your work subject to the terms of the CC BY license." (다른 창작자가 CC BY 조건에 따라 재사용할 수 있다.) — [YouTube Help: License types](https://support.google.com/youtube/answer/2797468?hl=en)
- Content ID 클레임이 걸린 영상에는 CC BY를 붙일 수 없다: "If there's a Content ID claim on your video, you can't add a Creative Commons Attribution license to your video." — [YouTube Help: License types](https://support.google.com/youtube/answer/2797468?hl=en)
- CC 영상은 검색 고급 필터로 찾을 수 있고, Data API에서는 `status.license` 값이 `creativeCommon`으로 표시된다. — [YouTube Help: License types](https://support.google.com/youtube/answer/2797468?hl=en), [Videos resource](https://developers.google.com/youtube/v3/docs/videos)
- 다운로드 도움말은 라이선스 구분 없이 "Note: You can't download other user's YouTube videos."라고 밝힌다. 오프라인 시청 수단으로는 YouTube Premium만 안내한다. — [YouTube Help: Download YouTube videos that you've uploaded](https://support.google.com/youtube/answer/56100?hl=en)
- 본인 영상은 Studio에서 720p 또는 360p MP4로, 또는 Google Takeout으로 전체를 내려받을 수 있다(영상당 하루 5회). — [YouTube Help: Download YouTube videos that you've uploaded](https://support.google.com/youtube/answer/56100?hl=en)
- 약관 1호의 예외는 "(a) as expressly authorized by the Service; or (b) with prior written permission from YouTube and, if applicable, the respective rights holders" 두 가지뿐이며, (b)는 YouTube의 허락과 권리자의 허락을 함께 요구한다. — [YouTube ToS](https://www.youtube.com/t/terms?hl=en&gl=KR)
- 개발자 정책의 다운로드/캐시 금지와 III.I.7 분리/수정 금지 조문에는 CC 영상이나 소유자 본인 영상에 대한 예외 문구가 없다. — [Developer Policies](https://developers.google.com/youtube/terms/developer-policies)

### Inferences
- CC BY 영상이라도 YouTube 서버에서 스트림을 추출하면 약관 1, 2, 3호 위반이라는 점은 달라지지 않는다. 약관 1호 (b)가 권리자 허락만으로는 부족하고 YouTube의 서면 허락까지 요구하는 구조이기 때문이다. CC 라이선스는 "그 저작물을 다른 경로로 확보했을 때" 변환과 재배포를 정당화할 뿐이다.
- 계약과 충돌하지 않는 경로는 두 가지다. (1) 채널 소유자가 공식 기능으로 내려받은 자기 영상 파일을 서비스에 올리는 방식, (2) CC BY 영상의 원본 파일을 창작자가 YouTube 밖(자체 사이트, Internet Archive 등)에서 배포하는 경우 그 파일을 쓰는 방식. 어느 쪽도 "유튜브 링크를 넣으면 변환"이라는 흐름은 아니다.
- 소유자가 OAuth로 로그인해도 Data API가 주는 것은 `fileDetails` 메타데이터뿐이어서, 소유자 인증만으로 API를 통해 영상 파일을 가져오는 자동화는 불가능하다. 소유자가 수동으로 내려받아 올려야 한다.

### Gaps
- YouTube가 CC BY 영상의 서드파티 다운로드를 공식적으로 용인하거나 문제 삼은 사례, 또는 이에 대한 공식 입장문은 찾지 못했다.
- 과거 YouTube 편집기에 있던 CC 영상 리믹스 기능처럼, 현재 플랫폼 내부에서 CC 영상을 재가공하게 해 주는 공식 기능이 남아 있는지는 확인하지 못했다.
