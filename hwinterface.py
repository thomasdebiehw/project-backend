from RPi import GPIO
import time

a = "running"


def main():
    try:
        while True:
            print(a)
            time.sleep(1)

    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()
        print("gestopt")


if __name__ == '__main__':
    main()
