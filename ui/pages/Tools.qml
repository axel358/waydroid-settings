import QtQuick 2.15
import QtQuick.Controls 2.15 as Controls
import QtQuick.Layouts 1.2
import org.kde.kirigami 2.20
import org.kde.kirigamiaddons.labs.mobileform 0.1
import Qt.labs.platform 1.1

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
                    onClicked: installApkDialog.open()
                }

                FormDelegateSeparator {}

                FormSwitchDelegate {
                    id: softKbSwitch
                    text: "Disable soft keyboard"
                    onCheckedChanged : backend.onSoftKbSwitchChanged(checked)
                }

                FormDelegateSeparator {}

                FormSwitchDelegate {
                    id: navButtonsSwitch
                    text: "Disable Android navigation buttons"
                    onCheckedChanged : backend.onNavButtonsSwitchChanged(checked)
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
                    onClicked: backend.onRestartContainerClicked()
                }

                FormDelegateSeparator {}

                FormSwitchDelegate {
                    text: "Freeze"
                    onCheckedChanged : backend.onFreezeSwitchChanged(checked)
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
                    onClicked: backend.onRestartSessionClicked()
                }

                FormDelegateSeparator {}

                FormButtonDelegate {
                    text: "Stop"
                    onClicked: backend.onStopSessionClicked()
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

    FileDialog {
        id: installApkDialog
        title: "Select apk"
        fileMode: FileDialog.OpenFile
        onAccepted: {
            backend.installApk(file)
        }
    }

    Connections {
        target: backend

        function onNavButtonsChanged (checked) {
            navButtonsSwitch.checked = checked
        }

        function onSoftKbChanged (checked) {
            softKbSwitch.checked = checked
        }
    }
}
