from dataclasses import dataclass


@dataclass(frozen=True)
class T:
    toolbar_title = "Ergebnis der Onlineprüfung"
    toolbar_back = "Zurück zur Bearbeitung der Aufgabe"

    compiler_text = "Ihr Programm wurde mit folgendem Kommando übersetzt:"

    error_text = (
        "Es traten Fehler- oder Warnmeldungen beim Übersetzen Ihres Programms auf!"
    )
    error_secondary_text = "Beheben Sie diese  Probleme und probierens Sie es erneut."
    error_button_text = (
        "Trotzdem Abgeben [b](Sie werden das Testat nicht bestehen!)[/b]"
    )

    pass_text = "Es traten keine Fehler- oder Warnmeldungen beim Übersetzen Ihres Programms auf!"
    pass_secondary_text = "Sie können Ihren Quellcode nun Abgeben."
    pass_button_text = "Testat Abgeben"
