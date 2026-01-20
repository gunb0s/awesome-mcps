# Notification Hook

macOS 시스템 알림을 통해 Claude Code 응답 완료를 알려주는 훅입니다.

## Features

- Claude Code 응답 완료 시 macOS 알림 표시
- "Glass" 사운드와 함께 알림
- 추가 설치 불필요 (macOS 내장 `osascript` 사용)

## Installation

1. `settings.json`의 내용을 Claude Code 설정에 복사합니다:

```bash
# 현재 설정 확인
cat ~/.claude/settings.json

# 설정 파일 편집
vim ~/.claude/settings.json
```

2. 또는 직접 설정 파일에 hooks 섹션을 추가합니다:

```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "osascript -e 'display notification \"Response complete\" with title \"Claude Code\" sound name \"Glass\"'"
          }
        ]
      }
    ]
  }
}
```

## Hook Events

| Event | Description |
|-------|-------------|
| `Stop` | Claude 응답 완료 시 실행 |

## Customization

### 알림 메시지 변경

```bash
osascript -e 'display notification "YOUR MESSAGE" with title "YOUR TITLE" sound name "Glass"'
```

### 사운드 변경

사용 가능한 사운드 목록:
- `Glass`
- `Ping`
- `Pop`
- `Purr`
- `Sosumi`
- `Submarine`

```bash
# 예: Ping 사운드 사용
osascript -e 'display notification "Response complete" with title "Claude Code" sound name "Ping"'
```

### 소리 없이 알림만

```bash
osascript -e 'display notification "Response complete" with title "Claude Code"'
```

## Verification

1. Claude Code 실행
2. 아무 질문이나 입력
3. 응답 완료 시 macOS 알림 확인

## Requirements

- macOS (osascript 내장)
- Claude Code

## Troubleshooting

### 알림이 표시되지 않는 경우

1. 시스템 환경설정 > 알림 센터에서 "터미널" 또는 Claude Code 알림이 허용되어 있는지 확인
2. 방해금지 모드가 꺼져있는지 확인

### 소리가 나지 않는 경우

1. 시스템 볼륨 확인
2. 시스템 환경설정 > 사운드에서 알림음 볼륨 확인
