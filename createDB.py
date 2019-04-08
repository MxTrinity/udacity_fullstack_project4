#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Base, User, Category, Item

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# clean up the db to avoid duplicates on rerun
session.query(Category).delete()
session.query(Item).delete()
session.commit()

# The root User, none of these items can be edited
user = User(username='SRD', email='WoTCfake1@gmail.com',
            picture='https://pbs.twimg.com/profile_images' +
            '/3372183710/f505b33cd78c1999fe6d9bd8a59fe59d_400x400.jpeg')
session.add(user)
session.commit()

# Create categories
weapons = Category(user_id=1, name="Weapons")
session.add(weapons)
session.commit()

armor = Category(user_id=1, name="Armor")
session.add(armor)
session.commit()

tools = Category(user_id=1, name="Artisan's Tools")
session.add(tools)
session.commit()

misc = Category(user_id=1, name="Miscellaneous Items")
session.add(misc)
session.commit()

magic = Category(user_id=1, name="Magic Items")
session.add(magic)
session.commit()


# MAKE ALL THE ITEMS

backpack = Item(user_id=1, name="Backpack",
                description="Holds your gear.",
                category=misc)
session.add(backpack)
session.commit()

carpentryTool = Item(user_id=1, name="Carpenter's Tools",
                     description="Used for building structural wooden items.",
                     category=tools)
session.add(carpentryTool)
session.commit()

shortsword = Item(user_id=1, name="Shortsword",
                  description="A medium bladed weapon. Use one in both hands.",
                  category=weapons)
session.add(shortsword)
session.commit()

dagger = Item(user_id=1, name="Dagger",
              description="A short bladed weapon. " +
              "It is very versatile and can be used with one hand.",
              category=weapons)
session.add(dagger)
session.commit()

leatherArmor = Item(user_id=1, name="Leather Armor",
                    description="Flexible leather armor. " +
                    "Offers nimble wearers more protection.",
                    category=armor)
session.add(leatherArmor)
session.commit()

rope = Item(user_id=1, name="Rope",
            description="20m of rope.",
            category=misc)
session.add(rope)
session.commit()

waterskin = Item(user_id=1, name="Waterskin",
                 description="Holds a quart of water.",
                 category=misc)
session.add(waterskin)
session.commit()

masonTool = Item(user_id=1, name="Mason's Tools",
                 description="Used for working with stone," +
                 " or making stonecraft.",
                 category=tools)
session.add(masonTool)
session.commit()

shortbow = Item(user_id=1, name="Shortbow",
                description="A small wooden bow. " +
                "Easy to use but limited range.",
                category=weapons)
session.add(shortbow)
session.commit()

crossbow = Item(user_id=1, name="Light Crossbow",
                description="A sturdy crossbow." +
                " Easy to use, hard to load, very effective.",
                category=weapons)
session.add(crossbow)
session.commit()

torch = Item(user_id=1, name="Torch",
             description="Can be ignited to create light in dark places.",
             category=misc)
session.add(torch)
session.commit()

rations = Item(user_id=1, name="Rations",
               description="One portable meal of preserved food.",
               category=misc)
session.add(rations)
session.commit()

breastplate = Item(user_id=1, name="Breastplate",
                   description="A metal armor covering the torso. " +
                   "Dexterity is required to protect the limbs.",
                   category=armor)
session.add(breastplate)
session.commit()

smithTool = Item(user_id=1, name="Smith's Tools",
                 description="Used for metalwork and repairs.",
                 category=tools)
session.add(smithTool)
session.commit()

greatsword = Item(user_id=1, name="Greatsword",
                  description="A two handed massive sword. " +
                  "It inflicts maximum damage in melee.",
                  category=weapons)
session.add(greatsword)
session.commit()

longsword = Item(user_id=1, name="Longsword",
                 description="A versatile sword can be used " +
                 "with both hands for more damage.",
                 category=weapons)
session.add(longsword)
session.commit()

fullPlate = Item(user_id=1, name="Plate Armor",
                 description="A full suit of metal armor. Maximum " +
                 "protection but requires high Strength to wear.",
                 category=armor)
session.add(fullPlate)
session.commit()

thiefTool = Item(user_id=1, name="Thieves' Tools",
                 description="Used many theiving activities, " +
                 "including picking locks.",
                 category=tools)
session.add(thiefTool)
session.commit()

whip = Item(user_id=1, name="Whip",
            description="A melee weapon with extended reach.",
            category=weapons)
session.add(whip)
session.commit()

longbow = Item(user_id=1, name="Longbow",
               description="A large heavy bow. " +
               "Does high damage at an incredible range.",
               category=weapons)
session.add(longbow)
session.commit()

shield = Item(user_id=1, name="Shield",
              description="A basic shield. Offers additional" +
              " protection to anyone regardless of armor.",
              category=armor)
session.add(shield)
session.commit()

herbalismTool = Item(user_id=1, name="Herbalism Kit",
                     description="Used for identifying natural materials " +
                     "and making tinctures from flora.",
                     category=tools)
session.add(herbalismTool)
session.commit()

heavyCrossbow = Item(user_id=1, name="Heavy Crossbow",
                     description="A massive crossbow. " +
                     "Does maximum damage at an extended range.",
                     category=weapons)
session.add(heavyCrossbow)
session.commit()

quiver = Item(user_id=1, name="Quiver",
              description="Holds 20 arrows for your ranged weapons",
              category=misc)
session.add(quiver)
session.commit()

missileWand = Item(user_id=1, name="Wand of Magic Missile",
                   description="Allows the user to cast Magic Missiles!",
                   category=magic)
session.add(missileWand)
session.commit()
