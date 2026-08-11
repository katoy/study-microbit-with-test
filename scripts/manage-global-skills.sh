#!/bin/bash

# micro:bit custom skills をグローバル設定に登録/削除するスクリプト
# 対応: claude, agy, codex, copilot

set -e

# スクリプト定義
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
SKILLS_DIR="$PROJECT_ROOT/skills"

# 対応するエージェント
AGENTS=("claude" "agy" "codex" "copilot")

# カラー定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 関数定義
print_header() {
    echo -e "${BLUE}=== Micro:bit Custom Skills Manager ===${NC}"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

# スキルディレクトリの確認
check_skills_dir() {
    if [ ! -d "$SKILLS_DIR" ]; then
        print_error "Skills ディレクトリが見つかりません: $SKILLS_DIR"
        exit 1
    fi

    local skill_count=$(ls -d "$SKILLS_DIR"/*/ 2>/dev/null | wc -l)
    if [ "$skill_count" -eq 0 ]; then
        print_error "スキルが見つかりません: $SKILLS_DIR"
        exit 1
    fi

    print_success "スキルディレクトリを確認: $SKILLS_DIR ($skill_count 個のスキル)"
}

# スキル一覧を取得
get_skills() {
    ls -d "$SKILLS_DIR"/*/ 2>/dev/null | xargs -I {} basename {} || echo ""
}

# スキルをエージェントに追加
add_skills() {
    local agent=$1
    local agent_config="$HOME/.$agent"
    local agent_skills_dir="$agent_config/skills"

    # エージェント設定ディレクトリが存在するか確認
    if [ ! -d "$agent_config" ]; then
        print_warning "$agent の設定ディレクトリが見つかりません: $agent_config"
        echo "  スキップします"
        return 1
    fi

    # skills ディレクトリを作成
    mkdir -p "$agent_skills_dir"

    local added_count=0
    for skill in $(get_skills); do
        local skill_path="$SKILLS_DIR/$skill"
        local link_path="$agent_skills_dir/$skill"

        # 既存のリンク/ファイルを削除
        if [ -e "$link_path" ] || [ -L "$link_path" ]; then
            rm -f "$link_path"
        fi

        # シンボリックリンクを作成
        if ln -s "$skill_path" "$link_path"; then
            ((added_count++))
        else
            print_error "  Failed to link: $skill"
        fi
    done

    if [ "$added_count" -gt 0 ]; then
        print_success "$agent に $added_count 個のスキルを追加しました"
        return 0
    else
        print_error "$agent にスキルを追加できませんでした"
        return 1
    fi
}

# スキルをエージェントから削除
remove_skills() {
    local agent=$1
    local agent_config="$HOME/.$agent"
    local agent_skills_dir="$agent_config/skills"

    # skills ディレクトリが存在しないか確認
    if [ ! -d "$agent_skills_dir" ]; then
        print_warning "$agent のスキルディレクトリが見つかりません: $agent_skills_dir"
        return 1
    fi

    local removed_count=0
    for skill in $(get_skills); do
        local link_path="$agent_skills_dir/$skill"

        # シンボリックリンクを削除
        if [ -L "$link_path" ] || [ -e "$link_path" ]; then
            if rm -f "$link_path"; then
                ((removed_count++))
            else
                print_error "  Failed to remove: $skill"
            fi
        fi
    done

    if [ "$removed_count" -gt 0 ]; then
        print_success "$agent から $removed_count 個のスキルを削除しました"
        return 0
    else
        print_warning "$agent に登録されたスキルが見つかりません"
        return 1
    fi
}

# ステータス表示
show_status() {
    echo
    print_info "スキル一覧:"
    for skill in $(get_skills); do
        echo "  - $skill"
    done

    echo
    print_info "エージェント別の登録ステータス:"
    for agent in "${AGENTS[@]}"; do
        local agent_skills_dir="$HOME/.$agent/skills"

        if [ ! -d "$agent_skills_dir" ]; then
            echo -e "  ${YELLOW}[$agent]${NC} 設定ディレクトリなし"
            continue
        fi

        local skill_count=0
        for skill in $(get_skills); do
            if [ -L "$agent_skills_dir/$skill" ]; then
                ((skill_count++))
            fi
        done

        if [ "$skill_count" -gt 0 ]; then
            echo -e "  ${GREEN}[$agent]${NC} $skill_count 個のスキルが登録されています"
        else
            echo -e "  ${YELLOW}[$agent]${NC} スキルが登録されていません"
        fi
    done
}

# ヘルプ表示
show_help() {
    cat << 'EOF'
使用方法: manage-global-skills.sh <command> [agents...]

コマンド:
  add <agents>      指定したエージェントにスキルを追加
  remove <agents>   指定したエージェントからスキルを削除
  status            全エージェントのステータスを表示
  help              このヘルプを表示

エージェント:
  claude            Claude (default: ~/.claude/)
  agy               Agy (default: ~/.agy/)
  codex             Codex (default: ~/.codex/)
  copilot           Copilot (default: ~/.copilot/)

例:
  # claude に追加
  ./manage-global-skills.sh add claude

  # 複数のエージェントに追加
  ./manage-global-skills.sh add claude agy codex copilot

  # claude から削除
  ./manage-global-skills.sh remove claude

  # ステータス表示
  ./manage-global-skills.sh status
EOF
}

# メイン処理
main() {
    print_header

    # コマンドの確認
    if [ $# -eq 0 ]; then
        print_error "コマンドを指定してください"
        echo
        show_help
        exit 1
    fi

    local command=$1
    shift

    # スキルディレクトリの確認
    check_skills_dir
    echo

    case "$command" in
        add)
            if [ $# -eq 0 ]; then
                print_error "エージェントを指定してください"
                show_help
                exit 1
            fi

            for agent in "$@"; do
                if [[ ! " ${AGENTS[@]} " =~ " ${agent} " ]]; then
                    print_error "サポートされていないエージェント: $agent"
                    continue
                fi
                add_skills "$agent" || true
            done
            show_status
            ;;

        remove)
            if [ $# -eq 0 ]; then
                print_error "エージェントを指定してください"
                show_help
                exit 1
            fi

            for agent in "$@"; do
                if [[ ! " ${AGENTS[@]} " =~ " ${agent} " ]]; then
                    print_error "サポートされていないエージェント: $agent"
                    continue
                fi
                remove_skills "$agent" || true
            done
            show_status
            ;;

        status)
            show_status
            ;;

        help|--help|-h)
            show_help
            ;;

        *)
            print_error "不明なコマンド: $command"
            show_help
            exit 1
            ;;
    esac

    echo
}

# スクリプト実行
main "$@"
