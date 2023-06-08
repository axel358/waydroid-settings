import QtQuick 2.15
import QtQuick.Layouts 1.3
import org.kde.kirigami 2.20

NavigationTabButton {
    property var page: applicationWindow().getPage(text)

    Layout.fillWidth: true
    width: column.width - column.Layout.leftMargin - column.Layout.rightMargin

    checked: pageStack.currentItem === page

    onClicked: {
        if (applicationWindow().pageStack.currentItem !== page) {
            applicationWindow().switchToPage(page, 0);
        }
    }
}
