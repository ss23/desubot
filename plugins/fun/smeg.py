from motobot import command
from random import choice


directives = [
    ('#003', 'By joining Star Corps each individual tacitly consents to give up his inalienable rights to life, liberty and adequate toilet facilities.'),
    ('#005', 'Computers guilty of gross negligence, leading to the endangerment of personnel, may be replaced by a backup computer.'),
    ('#112', 'States that a living crewmember always outranks a mechanoid.'),
    ('#121', 'No exploding in the Drive Room.'),
    ('#142', 'States that in a hostage demand situation, a hologrammtic crew member is entirely expendable.'),
    ('#147', 'Crew members are expressly forbidden from leaving their vessel except on permission of a permit. Permits can only be issued by the Chief Navigation Officer, who is expressly forbidden from issuing them except on production of a permit.'),
    ('#175', 'No running in the corridors. This was a rare occasion where Rimmer actually got a SCD right; at the time Kryten was going off to fetch some clothes for a naked Irene Edgington.'),
    ('#195', 'States that in an emergency power situation, a hologrammatic crewmember must lay down his life in order that the living crew-members might survive.'),
    ('#312', 'States that crew members in quarantine must be provided with minimum leisure facilities, which Rimmer takes to mean: a chess set with 31 missing pieces, a knitting magazine with a pull-out special on crocheted hats, a puzzle magazine with all the crosswords completed and a video of the excellent cinematic treat, "Wall-Papering, Painting And Stippling A DIY Guide.'),
    ('#349', 'Any officer found to have been slaughtered and replaced by a shape-changing chameleonic life form shall forfeit all pension rights.'),
    ('#497', 'When a crewmember has run out of credits, food or drink may not be supplied until the balance is restored'),
    ('#592', 'In an emergency situation involving two or more officers of equal rank, seniority will be given to whichever officer can programme a VCR.'),
    ('#595', 'Any member of the crew who has been in anywhere that carries disease must go into quarantine.'),
    ('#596 The crews files are for the eyes of the Captain only', ''),
    ('#597', 'One berth per registered crew member.'),
    ('#699', 'States that crew members may demand a re-screening after five days in quarantine showing no ill effect.'),
    ('#723', 'Terraformers are expressly forbidden from recreating Swindon. .'),
    ('#997', "Work done by an officer's doppleganger in a parallel universe cannot be claimed as overtime."),
    ('#1694', 'During temporal disturbances, no questions shall be raised about any crew member whose timesheet shows him or her clocking off 187 years before he clocked on.'),
    ('#1742', 'No member of the Corps should ever report for active duty in a ginger toupee.'),
    ('#1743', 'No registered vessel should attempt to traverse an asteroid belt without deflectors.'),
    ('#5796', 'No officer above the rank of mess sergeant is permitted to go into combat with pierced nipples.'),
    ('#5797', 'Possibly something to do with a crew member being unable to enter the ship for the safety of the crew when in an area of chameleonic lifeforms, although it could be that Kryten just decided to give up arguing with Rimmer rather than Rimmer quoting a valid directive.'),
    ('#7214', 'To preserve morale during long-haul missions, all male officers above the rank of First Technician must, during panto season, be ready to put on a dress and a pair of false breasts.'),
    ('#7713', 'States that the log must be kept up to date at all times with current service records, complete mission data and a comprehensive and accurate list of all crew birthdays so that senior officers may avoid bitter and embarrassing silences when meeting in the corridor with subordinates who have not received a card.'),
    ('#34124', 'No officer with false teeth should attempt oral sex in zero gravity.'),
    ('#43872', 'Suntans will be worn during off-duty hours only.'),
    ('#68250 Is never quoted, but is known to be impossible without at least one live chicken and a rabbi and involves sacrificing poultry, presumably the Jewish ritual "Kapparot"', ''),
    ('#196156', "Any officer caught sniffing the saddle of the exercise bicycle in the women's gym will be discharged without trial."),
    ('#1947945', 'A mechanoid may issue orders to human crew members if the lives of said crew members are directly or indirectly under threat from a hitherto unperceived source and there is inadequate time to explain the precise nature of the enormous and most imminent death threat.'),
    ('#5724368217968/B', 'At all times show your allegiance to Red Dwarf in the US by picking up your phone and calling your local public television station with your pledge.'),
    ('#39436175880932/B', 'All nations attending the conference are only allocated one parking space.'),
    ('#39436175880932/C', "POW's have a right to non-violent constraint."),
    ('UNKNOWN', "It is our primary overriding duty to contact other life forms, exchange information, and, wherever possible, bring them home.'"),
    ('UNKNOWN', 'In order to prevent gender ambiguity, all prisoners without a penis will be classified as female.'),
    ('UNKNOWN', 'Space Corps super chimps committing acts of indecency in zero gravity will lose all banana privileges.'),
    ('UNKNOWN', 'Any unnecessary ship should dispose of itself by flying straight into the nearest sun.'),
]


@command('smeg')
def snuggle_command(bot, context, message, args):
    """ Gives a Space Corps Directive. """
    return 'Space Corps Directive {}: {}'.format(*choice(directives))
