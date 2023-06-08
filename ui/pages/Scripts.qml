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
                model: ListModel {
                    ListElement {
                        name: "Bill Smith"
                        number: "555 3264"
                    }
                    ListElement {
                        name: "John Brown"
                        number: "555 8426"
                    }
                    ListElement {
                        name: "Sam Wise"
                        number: "555 0473"
                    }
                    ListElement {
                        name: "Bill Smith"
                        number: "555 3264"
                    }
                    ListElement {
                        name: "John Brown"
                        number: "555 8426"
                    }
                    ListElement {
                        name: "Sam Wise"
                        number: "555 0473"
                    }
                }
                width: parent.width
                //height: 200

                delegate: RowLayout {
                    anchors.left: parent.left
                    anchors.right: parent.right

                    Icon {
                        source: "scriptnew"
                    }

                    Label {
                        text: model.name
                        Layout.fillWidth: true
                    }

                    ToolButton{
                        icon.name: "documentinfo"
                        onClicked: {
                        }
                    }

                    ToolButton{
                        onClicked: {
                        }
                        flat: true
                        icon.name: "media-playback-start-symbolic"
                    }
                }

            }
        }

        Card{
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
                    id: mainsession
                    initialWorkingDirectory: "$HOME"
                }
                Component.onCompleted: mainsession.startShellProgram();

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
