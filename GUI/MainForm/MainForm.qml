import QtQuick 2.6
import QtQuick.Window 2.2
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12
import QtQuick.Controls.Styles 1.4
import QtQuick.Controls 1.2 as OldControls

ApplicationWindow {
    id: root
    visible: true
    //        visibility: "FullScreen"
    width: 900
    height: 200
    title: qsTr("Hello World")
    objectName: "root"
    signal textUpdated(string text)

    menuBar: MenuBar {


        background: Rectangle {
            color: "#f2f2f2"
        }

        Menu {
            title: qsTr("&File")

            Action {
                text: qsTr("&Open")
            }
            Action {
                text: qsTr("&Save Result")
            }

            MenuSeparator { }

            Action {
                text: qsTr("&Quit")

                onTriggered: Qt.quit()
            }

        }


        Menu {
            title: qsTr("&Run")
            Action {
                text: qsTr("&Run Chomsky")
            }
            Action {
                text: qsTr("&Check For Chomsky")
            }
            Action {
                text: qsTr("&Run GreiBach")
            }
            Action {
                text: qsTr("&Check For GreiBach")
            }
        }
        Menu {
            title: qsTr("&Help")
            Action { text: qsTr("&About") }
        }
    }


    Rectangle {
        id: baseRect
        anchors.fill: parent
        objectName: "kia"
        Component.onCompleted: {
            manager.add_qobject(this)
        }

        Column {
            id: lineNumberColumnLayout
            x: 3
            y: 3
            width: 15
            height: baseRect.height
//            Layout.alignment: Qt.AlignTop
            spacing: 3

            ListView {
                anchors.fill: parent
                Layout.preferredWidth: 10
                Layout.fillHeight: true
                model: lineNumberModel
                delegate: Label {
//                    Layout.alignment: Qt.AlignLeft
                    text: index
                    height: 16

                }
            }
        }

        ColumnLayout {
            id     : colLayout
            anchors.top: baseRect.top
            anchors.bottom: baseRect.bottom
            anchors.right: baseRect.right
            anchors.left: lineNumberColumnLayout.right

            Rectangle {
                id: editorRect
                Layout.fillWidth: true
                Layout.fillHeight: true
                color: "#546e7a"
                Flickable {
                    id: flcik
                    anchors.fill: parent
                    contentHeight: editorRect.height + editorTextEdit.implicitHeight
                    contentWidth: editorRect.width
                    clip: true

                    TextEdit {
                        property int index: 1
                        objectName: "myButton"
                        id: editorTextEdit
                        anchors.fill: parent
                        anchors.topMargin: 3
                        anchors.leftMargin: 5
                        Layout.maximumHeight: flcik.height
                        color: "white"
                        onTextChanged:textUpdated(text)

                        onLineCountChanged: {
                            lineNumberModel.change_line_count(lineCount)
                        }
                    }
                }
            }
        }
    }

}



