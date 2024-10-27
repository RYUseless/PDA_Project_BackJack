import src.utils.funny as Funneh
import src.utils.CardGen as CardGeneration


def main():
    greeter_instance = Funneh.Greeter()
    greeter_instance.run()

    cardGen_instance = CardGeneration.Generation()
    cardGen_instance.setup()


if __name__ == '__main__':
    main()
