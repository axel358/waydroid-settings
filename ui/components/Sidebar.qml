import QtQuick 2.15
import QtQuick.Layouts 1.3
import QtQuick.Controls 2.15 as QQC2
import org.kde.kirigami 2.20

OverlayDrawer {
    id: drawer
    modal: false
    width: 100
    height: applicationWindow().height

    Theme.colorSet: Theme.Window
    Theme.inherit: false

    leftPadding: 0
    rightPadding: 0
    topPadding: 0
    bottomPadding: 0

    contentItem: ColumnLayout {
        spacing: 0

        AbstractApplicationHeader {
            Layout.fillWidth: true
        }

        QQC2.ScrollView {
            id: scrollView
            Layout.fillWidth: true
            Layout.fillHeight: true

            QQC2.ScrollBar.vertical.policy: QQC2.ScrollBar.AlwaysOff
            QQC2.ScrollBar.horizontal.policy: QQC2.ScrollBar.AlwaysOff
            contentWidth: -1 // disable horizontal scroll

            ColumnLayout {
                id: column
                width: scrollView.width
                spacing: 0

                SidebarItem {
                    icon.name: "settings-configure"
                    text: "Settings"
                }

                SidebarItem {
                    icon.name: "scriptnew"
                    text: "Scripts"
                }

                SidebarItem {
                    icon.name: "extension-symbolic"
                    text: "Tools"
                }

                SidebarItem {
                    icon.name: "address-book-new"
                    text: "Docs"
                }
            }
        }

        Separator {
            Layout.fillWidth: true
            Layout.rightMargin: Units.smallSpacing
            Layout.leftMargin: Units.smallSpacing
        }

        SidebarItem {
            icon.name: "help-about-symbolic"
            text: "About"
        }
    }
}
