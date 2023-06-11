import QtQuick 2.15
import QtQuick.Controls 2.15 as Controls
import QtQuick.Layouts 1.2
import org.kde.kirigami 2.20
import org.kde.kirigamiaddons.labs.mobileform 0.1

ScrollablePage {
    id: root
    title: "Tools"
    
    ColumnView.fillWidth: false
    Theme.inherit: false
    Theme.colorSet: Theme.View

    ColumnLayout {
        spacing: Units.largeSpacing * 2

        FormCard {
            Layout.fillWidth: true

            contentItem: ColumnLayout {
                spacing: 0
                FormCardHeader{
                    title: "Android"
                }

                FormButtonDelegate {
                    text: "Increase system image size"
                    onClicked: resizeDialog.open()
                }

                FormDelegateSeparator {}

                FormButtonDelegate {
                    text: "Wipe all data(factory reset)"
                    onClicked: wipeDialog.open()
                }

                FormDelegateSeparator {}

                FormButtonDelegate {
                    text: "Install local apk"
                    onClicked: {}
                }

                FormDelegateSeparator {}

                FormSwitchDelegate {
                    id: enableJavascript
                    text: "Disable soft keyboard"
                    checked: true
                    onClicked: {}
                }

                FormDelegateSeparator {}

                FormSwitchDelegate {
                    id: loadImages
                    text: "Disable Android navigation buttons"
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
                    title: "Container"
                }
                FormButtonDelegate {
                    text: "Restart"
                    onClicked: {}
                }

                FormDelegateSeparator {}

                FormSwitchDelegate {
                    text: "Freeze"
                    checked: true
                    onClicked: {}
                }
            }
        }

        FormCard {
            Layout.fillWidth: true

            contentItem: ColumnLayout {
                spacing: 0
                FormCardHeader{
                    title: "Session"
                }
                FormButtonDelegate {
                    text: "Restart"
                    onClicked: {}
                }

                FormDelegateSeparator {}

                FormButtonDelegate {
                    text: "Stop"
                    onClicked: {}
                }
            }
        }
    }

    PromptDialog {
        id: resizeDialog
        title: "Resize image"
        showCloseButton: false

        ColumnLayout {
            spacing: Units.largeSpacing

            Controls.Label {
                text: "Current size 2Gb"
            }
            Controls.TextField {
                Layout.fillWidth: true
                placeholderText: qsTr("New size")
            }
        }

        standardButtons: Dialog.Ok | Dialog.Cancel
        onAccepted: showPassiveNotification("Resizing image...")
    }

    PromptDialog {
        id: wipeDialog
        showCloseButton: false
        title: "Factory reset"
        subtitle: "This will delete all user installed apps and settings. This cannot be undone"
        standardButtons: Dialog.Ok | Dialog.Cancel
        onAccepted: showPassiveNotification("Deleting all your kitty pics...")
    }
}