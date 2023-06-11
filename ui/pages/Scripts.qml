import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.2
import org.kde.kirigami 2.20
import QMLTermWidget 1.0
import org.kde.kirigamiaddons.labs.mobileform 0.1 as MobileForm

Page {
    id: root
    title: "Scripts"
    
    ColumnView.fillWidth: false
    Theme.inherit: false
    Theme.colorSet: Theme.View

    ColumnLayout {
        anchors.fill: parent
        spacing: Units.largeSpacing * 2

        ScrollView {
            Layout.fillWidth: true
            Layout.fillHeight: true
            ScrollBar.horizontal.policy: ScrollBar.AlwaysOff

            ListView {
                id: listView
                model: backend.scripts_model
                width: parent.width

                delegate: RowLayout {
                    anchors.left: parent.left
                    anchors.right: parent.right

                    Icon {
                        source: "scriptnew"
                    }

                    Label {
                        text: name
                        Layout.fillWidth: true
                    }

                    ToolButton{
                        icon.name: "documentinfo"
                        onClicked: {
                            terminal.run(path + " -h")
                        }
                    }

                    ToolButton{
                        onClicked: {
                            //backend.run_script(path)
                            terminal.run(path)
                        }
                        flat: true
                        icon.name: "media-playback-start-symbolic"
                    }
                }

            }
        }

        Card {
            Layout.fillWidth: true
            height: 150
            implicitHeight: height

            QMLTermWidget {
                id: terminal
                anchors.fill: parent
                height: parent.height
                font.family: "Monospace"
                font.pointSize: 11
                //colorScheme: "default"

                session: QMLTermSession{
                    id: termSession
                    initialWorkingDirectory: "$HOME"
                }


                function run(command) {
                    session.sendText(command)
                    pressKey(Qt.Key_Enter, Qt.NoModifier, true)
                }

                function pressKey(key, modifiers, pressed, nativeScanCode, text) {
                    simulateKeyPress(key, modifiers, pressed, nativeScanCode, text);
                    forceActiveFocus();
                }
                Component.onCompleted: termSession.startShellProgram();

                QMLTermScrollbar {
                    terminal: terminal
                    width: 20
                    Rectangle {
                        opacity: 0.4
                        anchors.margins: 5
                        radius: width * 0.5
                        anchors.fill: parent
                    }
                }

            }
        }
    }

    Component.onCompleted: terminal.forceActiveFocus();

}
