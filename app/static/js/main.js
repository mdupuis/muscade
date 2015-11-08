function nextDivSibling(node) {
    while (node != null) {

        var next = node.nextSibling;
        if (next.nodeName == "DIV") {
            return next;
        } else {
            node = next;
        }
    }
    return null;
}

function previousDivSibling(node) {
    while (node != null) {

        var next = node.previousSibling;
        if (next.nodeName == "DIV") {
            return next;
        } else {
            node = next;
        }
    }
    return null;
}