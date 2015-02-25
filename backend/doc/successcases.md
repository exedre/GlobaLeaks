# Success Cases specification

**Success Cases** are published release of content that a GlobaLeaks node perform during the lifecicle.

At the moment do not exist a collection of those results, but they represent the very impact of GlobaLeaks in the World, and in a more refined analysis, they represent the impact of a specific Node in the World or at least in the context of interest.


## Basic assumption

The leaked document and/or the submitted material is a [Primary Source](https://en.wikipedia.org/wiki/Primary_source)

The report product of the Receiver is the [Secondary Source](https://en.wikipedia.org/wiki/Secondary_source)

After a breaking news happen, also some tertiary sources cover the event.

The multi language and globally distributed nature of GlobaLeaks cause that no central index can exists, is essential delegate the duty of reporting on the Node.

In order to get the node motivated in publish constantly the success, we have to elaborate some positive feedback for the Node/Receiver.

Having different kind of Node running in the world, we have to credit the autorship of the publication to the Node ant (optionally) to the Receiver. 

We have to ask, to the current node adopters, to report also the past success, therefore a calendar able to make them set a past date is essential

## Goal

Every GlobaLeans installation, need to keep track all the secondary source published online, freely accessible by Internet, based on material receiver via the node itself.

Every secondary source has to be reported only once per Tip/History.

These data will became part of the **GlobaLeaks Node History**, one of the informative element that the future LeakDirectory users want to see. This global collection will show the result of a single node and of all our network.

Specification of LeakDirectory will follow, this text is intended only for the SuccessCase

## Consideration and proposal

Every node want that some information goes public, if an information remain private, or in knowledge of the receivers only, this is not a Success Case

In the media environment, the copy-paste is a quite common practice, so a single news has to be reported only once 

The Success Cases cannot be enforce as unique, by theory a node can flood its own statistic. Due to the small amount of node existing at the moment, we can accept this risk until a true issue arise.

The interface to propose the success case is visible by Admin and all the receivers. 

The interface to propose the success case, display all the success cased in a list.

In the future, every Tip can have some **exit status** usable in statistics, just to mention some kind of possible outcomes:

  * useless submission - not managed
  * not enough information to complete the report - managed but without success
  * good submission - managed 

The status of good submission, can request the adding of a Success Case. This should or should not implemented in the future, but now (February 2015) we have to provide a dedicated interface 

## High level Format

  * Date (of the publication)
  * Link to the secondary source
  * Node name: (default the node.name, but can be changed, and is proposed to keep the same at every new addings), e.g.: WildLeaks, IRPI, PubLeaks.NL
  * Sub Author: optional, see below

WildLeaks case ( without Sub-Author):

    WildLeaks - 25/12/2010 - Berlusconi charged with Ivory smuggling 

PubLeaks.NL case ( with Sub-Author):

    PubLeaks.NL - De Corrispondant - 25/12/2010 - Fresh weed for xmas


## Internal Format

Database:

  id (as default),
  creation_date (as default),
  publication_date (added by the use via calendar, datetime format),
  link (unicode),
  author (JSON, keys: *node* and *author*)

REST:

  GET /successcases (accessible by everyone): return the list of all the success cases
  POST /successcases (accessible by admin and receiver): append a new S.C. to the collection
  PUT /successcases/id (admin and receiver): edit a previous existing S.C.
  DELETE /successcases/id (admin and reeiver): delete a previous existing S.C.


