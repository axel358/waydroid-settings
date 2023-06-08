import QtQuick 2.11
import QtQuick.Controls 2.4
import QtQuick.Layouts 1.2
import org.kde.kirigami 2.11 as Kirigami

Kirigami.ApplicationWindow {
    id: root
    title: "Waydroid Settings"

    // needs to work with 360x720 (+ panel heights)
    minimumWidth: 300
    minimumHeight: minimumWidth + 1
    width: Kirigami.Settings.isMobile ? 360 : 650
    height: Kirigami.Settings.isMobile ? 720 : 500

    pageStack.globalToolBar.canContainHandles: true
    pageStack.globalToolBar.style: Kirigami.ApplicationHeaderStyle.ToolBar
    pageStack.globalToolBar.showNavigationButtons: Kirigami.ApplicationHeaderStyle.ShowBackButton;
    pageStack.popHiddenPages: true
    pageStack.columnView.columnResizeMode: Kirigami.ColumnView.SingleColumn
    
    property bool isWidescreen: root.width >= 500
    onIsWidescreenChanged: changeNav(isWidescreen);

    contextDrawer: Kirigami.ContextDrawer {}
    
    Kirigami.PagePool {
        id: pagePool
    }
    
    Component.onCompleted: {
        // initial page and nav type
        switchToPage(getPage("Settings"), 1);
        changeNav(isWidescreen);
    }
    
    function switchToPage(page, depth) {
        // pop pages above depth
        while (pageStack.depth > depth) pageStack.pop();
        while (pageStack.layers.depth > 1) pageStack.layers.pop();
        
        pageStack.push(page);
    }
    
    function getPage(name) {
        switch (name) {
            case "Settings": return pagePool.loadPage("pages/Settings.qml");
            case "Scripts": return pagePool.loadPage("pages/Scripts.qml");
            case "Tools": return pagePool.loadPage("pages/Tools.qml");
            case "Docs": return pagePool.loadPage("pages/Docs.qml");
            case "About": return pagePool.loadPage("pages/About.qml");
        }
    }
    
    // switch between bottom toolbar and sidebar
    function changeNav(toWidescreen) {
        if (toWidescreen) {
            if (footer !== null) {
                footer.destroy();
                footer = null;
            }
            sidebarLoader.active = true;
            globalDrawer = sidebarLoader.item;
        } else {
            sidebarLoader.active = false;
            globalDrawer = null;
            
            let bottomToolbar = Qt.createComponent("components/BottomToolbar.qml")
            footer = bottomToolbar.createObject(root);
        }
    }
    
    Loader {
        id: sidebarLoader
        source: "components/Sidebar.qml"
        active: false
    }
}
