import QtQuick 2.15

Item {
    implicitWidth: 200
    implicitHeight: 100
    property string clockText: Qt.formatTime(new Date(), "hh:mm")
    Timer {
        interval: 1000
        running: true
        repeat: true
        onTriggered: clockText = Qt.formatTime(new Date(), "hh:mm")
    }
    Rectangle {
        anchors.fill: parent
        color: "#303b2d"
        radius: 12
        Text {
            anchors.centerIn: parent
            text: clockText
            color: "#eeeede"
            font.pixelSize: 32
        }
    }
}
