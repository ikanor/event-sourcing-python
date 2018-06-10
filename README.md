# Event Sourcing Python Demo

A Simple, Idiomatic, Event-Sourcing Pattern written in Python.

## Domain

This example implements a checkout operation on a basket. The two use cases are:

1. Add a new item to the basket
2. Check out the items in the basket

As a result, a `PAY_ORDER` command is generated so the payments service can start the transaction.

## Commands and Events

The saga comprehends:

* `BASKET_CREATED` (event): Triggered when a new user enters the shop.
* `ADD_ITEM` (command): Sent whenever the user adds an item to the basket.
* `ITEM_ADDED` (event): Broadcasted when the previous operation is consolidated.
* `CHECKOUT` (command): Sent when the user proceeds to the payment.
* `CHECKOUT_STARTED` (event): Broadcasted when checkout has been validated.
* `PAY_ORDER` (command): Same as the `CHECKOUT_STARTED` event.

## Design

There is a message receiver that controls the input stream. Whenever a new message arrives (no matter if it's a command or an event) it passes it onto the consumers.

There are two consumers. The first one stores the events so they can later be retrieved. The second one implements the Basket operations.

The Basket consumer actually delegates the business logic to a Basket model. The latter is the one in charge of recovering the basket status (with the rebuild operation) and also of deciding which are the next commands/events. This delegation helps separating the connector operations (fetch from persistence, talk to other APIs) from the pure business rules.

## Thanks To

To [Georgina Giannoukou](https://github.com/georginagi) and [Nacho Viejo](https://github.com/saski), who helped to refine this pattern. Also to [Ronny Ancorinni](https://github.com/ronnyanc) and [Fran Ortiz](https://github.com/Fortiz2305), who originally applied [Greg Young's demo](https://github.com/gregoryyoung/m-r) to Python.
