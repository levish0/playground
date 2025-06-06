import os

def list_text_files():
    """List all .txt files in the current directory."""
    return [f for f in os.listdir() if f.endswith('.txt')]

def read_file(filename):
    """Read and return the contents of a file."""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return "파일을 찾을 수 없습니다."
    except Exception as e:
        return f"파일을 읽는 중 오류가 발생했습니다: {e}"

def main():
    print("사용 가능한 텍스트 파일 목록:")
    files = list_text_files()
    
    if not files:
        print("텍스트 파일이 없습니다.")
        return
    
    while True:
        print("\n" + "="*50)
        print("사용 가능한 파일 목록:")
        for i, file in enumerate(files, 1):
            print(f"{i}. {file}")
        print("0. 종료")
        
        try:
            choice = input("\n읽을 파일 번호를 선택하세요 (0으로 종료): ")
            if choice == '0':
                print("프로그램을 종료합니다.")
                break
                
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(files):
                selected_file = files[choice_idx]
                print(f"\n[{selected_file} 내용]")
                print("-"*50)
                print(read_file(selected_file))
                print("-"*50)
                
                # 파일을 계속 볼지 선택
                while True:
                    cont = input("\n다른 파일을 보시겠습니까? (y/n): ").lower()
                    if cont in ['y', 'n']:
                        break
                    print("y 또는 n으로 답해주세요.")
                
                if cont == 'n':
                    print("프로그램을 종료합니다.")
                    break
            else:
                print("잘못된 선택입니다. 다시 시도해주세요.")
                
        except ValueError:
            print("숫자를 입력해주세요.")
        except Exception as e:
            print(f"오류가 발생했습니다: {e}")

if __name__ == "__main__":
    main()
