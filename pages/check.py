from nicegui import app, ui


def check_section(number, lesson):
    quiz = lesson.get('quiz')
    compare = lesson.get('compare')
    if not (quiz or compare):
        return

    with ui.column().classes('lesson-body items-start'):
        ui.label('Check yourself').classes('section-title')
        if quiz:
            _quiz(number, quiz)
        if compare:
            _compare(compare)


def _option_button(text, on_click):
    return ui.button(text, on_click=on_click, color=None) \
        .props('flat no-caps align=left').classes('glass-btn') \
        .style('white-space: normal; text-align: left; border-radius: 28px; max-width: 100%')


def _mark(button, state):
    """Show 'ok', 'bad' or (None) the neutral look on an option; the icon means colour isn't the only cue."""
    button.classes(remove='opt-ok opt-bad')
    button.props(remove='icon-right')
    if state:
        button.classes(f'opt-{state}')
        button.props(f'icon-right={"check" if state == "ok" else "close"}')


def _quiz(number, quiz):
    answered = {}
    best_store = app.storage.user.setdefault('quiz_best', {})
    score_label = ui.label().classes('subtitle')

    def refresh_score():
        if len(answered) == len(quiz):
            score = sum(answered.values())
            if score > best_store.get(str(number), -1):
                best_store[str(number)] = score
            score_label.set_text(f'Score: {score}/{len(quiz)} · Best: {best_store[str(number)]}/{len(quiz)}')
        elif str(number) in best_store:
            score_label.set_text(f'Best: {best_store[str(number)]}/{len(quiz)}')
        else:
            score_label.set_text('')

    for index, question in enumerate(quiz):
        with ui.card().classes('panel w-full q-mt-md'):
            ui.label(f'{index + 1}. {question["question"]}').classes('card-title')
            buttons = []
            result = ui.label().classes('body-text')
            retry = ui.button('Try again', color=None).props('flat no-caps').classes('glass-btn')
            result.set_visibility(False)
            retry.set_visibility(False)

            def pick(choice, index=index, question=question, buttons=buttons, result=result, retry=retry):
                correct = choice == question['answer']
                for button in buttons:
                    button.disable()
                _mark(buttons[choice], 'ok' if correct else 'bad')
                if correct:
                    result.set_text(f'Correct ✓ {question["explain"]}')
                else:
                    result.set_text('Incorrect. Try again.')
                result.set_visibility(True)
                retry.set_visibility(True)
                answered[index] = correct
                refresh_score()

            def reset(index=index, buttons=buttons, result=result, retry=retry):
                for button in buttons:
                    button.enable()
                    _mark(button, None)
                result.set_visibility(False)
                retry.set_visibility(False)
                answered.pop(index, None)
                refresh_score()

            retry.on_click(reset)
            # place options above the result: build them in a container before result
            with ui.column().classes('items-start gap-2') as options_box:
                for choice, text in enumerate(question['options']):
                    buttons.append(_option_button(text, lambda c=choice, p=pick: p(c)))
            options_box.move(target_index=1)
    refresh_score()


def _compare(compare):
    with ui.card().classes('panel w-full q-mt-lg'):
        ui.label('Which prompt is better?').classes('card-title')
        buttons = []
        result = ui.label().classes('body-text')
        retry = ui.button('Try again', color=None).props('flat no-caps').classes('glass-btn')
        result.set_visibility(False)
        retry.set_visibility(False)

        def pick(choice):
            for button in buttons:
                button.disable()
            correct = choice == compare['better']
            _mark(buttons[('a', 'b').index(choice)], 'ok' if correct else 'bad')
            if correct:
                result.set_text(f'Correct ✓ Prompt {compare["better"].upper()} is better. {compare["why"]}')
            else:
                result.set_text('Incorrect. Try again.')
            result.set_visibility(True)
            retry.set_visibility(True)

        def reset():
            for button in buttons:
                button.enable()
                _mark(button, None)
            result.set_visibility(False)
            retry.set_visibility(False)

        retry.on_click(reset)
        with ui.column().classes('items-start gap-2') as options_box:
            for key in ('a', 'b'):
                buttons.append(_option_button(f'{key.upper()}: {compare["prompt_" + key]}',
                                              lambda k=key: pick(k)))
        options_box.move(target_index=1)
