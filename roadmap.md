# Dshop


## The goal

Dshop is an educational project aimed at learning to work together using Github and Django. As a result, we will build an online store. To manage the project, we use tasks in [Clickup](https://clickup.com/), we use Kanban.

  During our work, we put special emphasis on:
  * using pull requests and working in a group
     * performing Code Review and learning how to create useful and friendly Code Reviews using good practices from [Google](https://google.github.io/eng-practices/review/reviewer/comments.html)
  * code purity, verified automatically using Github Actions
  * **pressure will be put on Test Driven Development based on pytest - tests will also be verified automatically**
  * building a sense of individual responsibility for their work in a team
  * building a friendly and open work culture in the team
  * learning together and sharing knowledge through
    * pair programming as a requirement. Use this as an opportunity to harden and share knowledge.
    * conversations on Discord
    * live meetings (recorded for those absent)
    * remote training sessions, organized as needed

The ultimate goal is to equip community members with soft and hard skills to help them land their first IT job or move up in their current one.

## Project Roadmap

The project will be developed incrementaly. We will make sure project is usable on milestones. The project will use well established frontend framework: [Bootstrap](https://getbootstrap.com/)

### MVP #1.
1. Initial setup of the project, including basic automation, basic user models (done).
2. Create products catalogue using vanilla Django templates. No variations, etc, just simple products catalogue with lightbox like products presentation - @Meise90 i @Knop-k i @Adam-Feliniak
3. Implement sitemaps for the entire products catalogue, using Test Driven Development. https://developers.google.com/search/docs/crawling-indexing/sitemaps/overview?hl=pl - @xtcprzemek i @yanazPL
4. Implement xml file for Ceneo. This is another great piece of code allowing to work with TDD: https://www.ceneo.pl/poradniki/Instrukcja-tworzenia-pliku-XML - @Memorisanka + xtcPrzemek
5. User account. Registration, management, editing, login and log out of the site. This also requires basic template view sites with placeholder for privacy policy. Do not implement reset password flow, yet. @sprzesmycki i @prezes.
6. Persistent shopping cart, using database as backend. This will allow user to put item in the cart on mobile and finish purchase on computer. @kvothe + @xtcPrzemek
7. Delivery method implementation: https://inpost.pl/integracja-z-inpost or similar @prezes + @memorisanka
8. Payment method implementation. Probably stripe. There is a project we can take over: https://github.com/HealthByRo/aa-stripe. @sprzesmycki @Memorisanka

### MVP#2
1. Integrate the whole Cart with products catalogue, payment and delivery so we can actually order something. 

### MVP #3.
1. Product variations, types, sizes, etc.
2. REST API to access the service (DRF, great to test TDD skills)

### MPV #4
1. Product warehouse and amount of products
TBD.
