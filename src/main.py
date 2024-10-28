import src.utils.funny as Funneh
import src.utils.CardGen as CardGeneration
import src.utils.gymnasium_src as GymMrdka


def main():
    greeter_instance = Funneh.Greeter()
    greeter_instance.run()

    cardGen_instance = CardGeneration.Generation()
    cardGen_instance.setup()

    gym_instance = GymMrdka.Run()
    gym_instance.placeholder()


if __name__ == '__main__':
    main()
