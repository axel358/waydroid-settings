import org.kde.kirigami 2.20

NavigationTabBar {
    id: root

    visible: height !== 0

    actions: [
        NavAction {
            text: "Settings"
            iconName: "settings-configure"
        },
        NavAction {
            text: "Scripts"
            iconName: "scriptnew"
        },
        NavAction {
            text: "Tools"
            iconName: "extension-symbolic"
        },
        NavAction {
            text: "Docs"
            iconName: "address-book-new"
        },
        NavAction {
            text: "About"
            iconName: "help-about-symbolic"
        }
    ]
} 
