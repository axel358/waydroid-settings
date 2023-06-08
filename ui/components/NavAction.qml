import org.kde.kirigami 2.20

Action {
    property var page: applicationWindow().getPage(text)
    checked: page === pageStack.currentItem
    onTriggered: {
        if (page  !== pageStack.currentItem) {
            applicationWindow().switchToPage(page, 0);
        }
    }
}
