import QtQuick 2.15
import QtQuick.Controls 2.15 as QQC2
import QtQuick.Window 2.15
import QtQuick.Layouts 1.15
import org.kde.kirigami 2.20
import org.kde.kirigamiaddons.labs.mobileform 0.1

ScrollablePage {
    id: page
    property var aboutData
    title: "About"

    ColumnLayout {
        width: parent.width
        spacing: Units.largeSpacing * 2

        FormCard {
            Layout.fillWidth: true
            contentItem: ColumnLayout {
                spacing: 0

                AbstractFormDelegate {
                    id: generalDelegate
                    Layout.fillWidth: true
                    background: Item{}
                    contentItem: RowLayout {
                        spacing: Units.smallSpacing * 2

                        Icon {
                            Layout.rowSpan: 3
                            Layout.preferredHeight: Units.iconSizes.huge
                            Layout.preferredWidth: height
                            Layout.maximumWidth: page.width / 3;
                            Layout.rightMargin: Units.largeSpacing
                            source: aboutData.icon
                        }

                        ColumnLayout {
                            Layout.fillWidth: true
                            spacing: Units.smallSpacing

                            Heading {
                                Layout.fillWidth: true
                                text: aboutData.displayName + " " + aboutData.version
                                wrapMode: Text.WordWrap
                            }

                            Heading {
                                Layout.fillWidth: true
                                level: 3
                                type: Heading.Type.Secondary
                                wrapMode: Text.WordWrap
                                text: aboutData.shortDescription
                            }
                        }
                    }
                }

                FormDelegateSeparator {}

                FormTextDelegate {
                    text: "License"
                    descriptionItem.textFormat: Text.PlainText
                    description: aboutData.license
                }

                FormTextDelegate {
                    text: "Copyright"
                    descriptionItem.textFormat: Text.PlainText
                    description: aboutData.copyright
                }
            }
        }

        FormCard {
            Layout.fillWidth: true
            contentItem: ColumnLayout {
                spacing: 0

                FormButtonDelegate {
                    id: getInvolvedDelegate
                    text: "Homepage"
                    onClicked: Qt.openUrlExternally(aboutData.homepage)
                    visible: aboutData.homepage !== undefined
                }

                FormDelegateSeparator { visible: aboutData.homepage  !== undefined }

                FormButtonDelegate {
                    id: donateDelegate
                    text: "Donate"
                    onClicked: Qt.openUrlExternally(aboutData.donateUrl)
                    visible: aboutData.donateUrl !== undefined
                }

                FormDelegateSeparator { visible: aboutData.donateUrl !== undefined }

                FormButtonDelegate {
                    id: bugDelegate
                    text: "Report a bug"
                    onClicked: Qt.openUrlExternally(aboutData.issueTracker)
                    visible: aboutData.issueTracker !== undefined
                }
            }
        }

        FormCard {
            Layout.fillWidth: true
            contentItem: ColumnLayout {
                spacing: 0

                FormCardHeader {
                    title: "Authors"
                    visible: aboutData.authors.length > 0
                    Layout.fillWidth: true
                }

                Repeater {
                    id: authorsRepeater
                    model: aboutData.authors
                    delegate: personDelegate
                }

                FormCardHeader {
                    title: "Credits"
                    visible: aboutData.credits.length > 0
                    Layout.fillWidth: true
                }

                Repeater {
                    id: repCredits
                    model: aboutData.credits
                    delegate: personDelegate
                }
            }
        }
    }

    Component {
        id: personDelegate

        AbstractFormDelegate {
            Layout.fillWidth: true
            background: Item {}
            contentItem: RowLayout {
                spacing: Units.smallSpacing * 2

                Avatar {
                    id: avatarIcon

                    property bool hasRemoteAvatar: false
                    implicitWidth: Units.iconSizes.medium
                    implicitHeight: implicitWidth
                    initialsMode: Avatar.ImageMode.AlwaysShowImage
                    name: modelData.name
                }

                ColumnLayout {
                    Layout.fillWidth: true
                    spacing: Units.smallSpacing

                    QQC2.Label {
                        Layout.fillWidth: true
                        text: modelData.name
                        elide: Text.ElideRight
                    }

                    QQC2.Label {
                        id: internalDescriptionItem
                        Layout.fillWidth: true
                        text: modelData.task
                        color: Theme.disabledTextColor
                        font: Theme.smallFont
                        elide: Text.ElideRight
                        visible: text !== ""
                    }
                }

                QQC2.ToolButton {
                    visible: typeof(modelData.emailAddress) !== "undefined" && modelData.emailAddress.length > 0
                    icon.name: "mail-sent"
                    QQC2.ToolTip.delay: Units.toolTipDelay
                    QQC2.ToolTip.visible: hovered
                    QQC2.ToolTip.text: qsTr("Send an email to %1").arg(modelData.emailAddress)
                    onClicked: Qt.openUrlExternally("mailto:%1".arg(modelData.emailAddress))
                }
            }
        }
    }
}
