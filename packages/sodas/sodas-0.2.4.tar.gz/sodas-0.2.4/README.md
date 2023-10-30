# SODAS Workflow Devops Tools

## DevTools 
### 개발 이유
* 알고리즘 개발을 하면서 data를 각 container 내에서 read / write를 하기 위한 코드가 필요했음
* 알고리즘을 개발할 때마다 위의 코드가 필수적으로 들어가야 했고 해당 코드를 실행하기 위한 환경변수가 많이 필요했기에 DX적으로 굉장히 좋지 않다고 생각함
* 더불어 각종 인가 코드를 환경 변수로 세팅해야 했기에 각종 보안 상으로도 좋지 않음
* 위와 같이 알고리즘을 개발하기 위해서 복잡한 설정을 해야하기 때문에 사실상 SODAS+ 팀 내부 인원이 아닌 이상 알고리즘을 개발하고 테스트하기 어렵다고 생각 (물론 팀 내부에서도 현재와 같은 구조에선 불필요한 코드 반복이 이뤄짐)
    * 따라서 분석 워크플로우 알고리즘 개발자를 위한 distribution 접근 라이브러리를 제작하기로 함

### 개발 진행 상황
- [x] 기본적인 패키지 작성과 패키지 테스트
    - [x] Object Storage
        - [x] Distribution read 함수
        - [x] Personal data read 함수
        - [x] write 함수
        - [x] Object Storage Library Test


    - [ ] ClickHouse
        - [ ] Distribution read 함수
        - [ ] Personal data read 함수
        - [ ] write 함수
        - [ ] Object Storage Library Test


    - [ ] PostgreSQL
        - [ ] Distribution read 함수
        - [ ] Personal data read 함수
        - [ ] write 함수
        - [ ] Object Storage Library Test


- [ ] Code Refactoring
    - [ ] 클래스화 
    - [ ] PEP8 lint 적용
    - [ ] Test code 작성
    

- [x] Pypi 등록을 위한 기본 코드 작성 
    * Pypi 등록 완료 (v0.1.2)
        ```
        pip install sodas
        ```


### Package 구조
* (추후 도식화 해서 추가할 예정)

### Documents
* (추후 추가될 예정입니다.)
