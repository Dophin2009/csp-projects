import QtQuick 2.0
import QtQuick.Layouts 1.11

Rectangle {
    id: page
    width: 480
    height: 720

    Column {
        spacing: 2

        Text {
            id: statusText
            text: gameState.status_text
            y: 30
            font.pointSize: 20; font.bold: true
        }

        GridView {
            cellWidth: 80; cellHeight: 80
            highlight: Rectangle { color: "lightsteelblue"; radius: 5 }
            focus: true


            model: gameState.piles
            // delegate: Text {
                // id: pileIndex
                // text: "fjakwlfj"
            // }
            delegate: Rectangle {
                id: wrapper
                color: "black"

                Text {
                    id: pileIndex
                    text: "fjakwlfj"
                }
            }
        }
    }
}
