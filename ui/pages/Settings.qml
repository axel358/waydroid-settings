import QtQuick.Layouts 1.2
import org.kde.kirigami 2.20
import org.kde.kirigamiaddons.labs.mobileform 0.1
import "../components"

ScrollablePage {
    id: root
    title: "Settings"
    
    ColumnView.fillWidth: false
    Theme.inherit: false
    Theme.colorSet: Theme.View

    // settings list
    ColumnLayout {
        spacing: Units.largeSpacing * 2

        FormCard {
            Layout.fillWidth: true

            contentItem: ColumnLayout {
                spacing: 0
                FormCardHeader{
                    title: "General"
                }
                FormSwitchDelegate {
                    id: enableJavascript
                    text: "Enable multi-window mode"
                    description: "Only works on Gnome/Mutter"
                    checked: true
                    onClicked: {}
                }

                FormDelegateSeparator {}

                FormSwitchDelegate {
                    id: loadImages
                    text: "Suspend the container on inactivity"
                    description: "Whether to suspend the container on inactivity"
                    checked: false
                    onClicked: {}
                }

                FormDelegateSeparator {}

                FormSwitchDelegate {
                    text: "Invert colors"
                    checked: false
                    onClicked: {}
                }

                FormDelegateSeparator {}

                FormButtonDelegate {
                    text: "Apps to exclude from free form"
                    checked: false
                    onClicked: {}
                }

                FormDelegateSeparator {}

                FormButtonDelegate {
                    text: "Apps to exclude from free form"
                    checked: false
                    onClicked: {}
                }
            }
        }

        FormCard {
            Layout.fillWidth: true

            contentItem: ColumnLayout {
                spacing: 0
                FormCardHeader{
                    title: "Windows"
                }
                FormSpinBoxDelegate {
                    label: "Window width"
                    onClicked: {}
                }

                FormDelegateSeparator { }

                FormSpinBoxDelegate {
                    label: "Window height"
                    onClicked: {}
                }
            }
        }
    }
}
