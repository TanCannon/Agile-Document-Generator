from . import generateUserStories
from . import generateSprintPlanning
from . import generateGanttChart
import time
cooldown_time = 2
def runAllPrompts(frd_path:str = None) -> None:
    generateUserStories.main(frd_path)
    print(f"sleep for {cooldown_time} second")
    time.sleep(cooldown_time)
    print('RESTARTED!')
    generateSprintPlanning.main()
    print(f"sleep for {cooldown_time} second")
    time.sleep(cooldown_time)
    print('RESTARTED!')
    generateGanttChart.main()

if __name__ == "__main__":
    frd_path = "./documents/DIG-ITS FRD_v2.pdf"
    print("Generating Documents...")
    generateUserStories.main(frd_path)

    print(f"sleep for {cooldown_time} second")
    time.sleep(cooldown_time)
    print('RESTARTED!')

    generateSprintPlanning.main()

    print(f"sleep for {cooldown_time} second")
    time.sleep(cooldown_time)
    print('RESTARTED!')

    generateGanttChart.main()
    print("Finished! Generated Documents.")

