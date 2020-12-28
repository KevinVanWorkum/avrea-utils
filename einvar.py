# reset all stats
!alias rs embed
<drac2>
stats = {"hp":133,"str":20,"dex":11,"con":20,"int":10,"wis":12,"char":8,"AC":19,"proficiency":4}
set_uvar("stats",dump_json(stats))
if len(&ARGS&) == 0:
    set_uvar("SD_now",5)
    set_uvar("HD_now",11)
    set_uvar("HP_now",133)
    set_uvar("AS_now",1)
    set_uvar("ID_now",1)
    set_uvar("WD_now",1)
if "%1%" == 'SD':
    set_uvar("SD_now",5) 
elif "%1%" == 'HD':
    set_uvar("HD_now",11) 
elif "%1%" == 'HP':
    set_uvar("HP_now",133) 
elif "%1%" == 'AS':
    set_uvar("AS_now",1)
elif "%1%" == 'ID':
    set_uvar("ID_now",1) 
elif "%1%" == 'WD':
    set_uvar("WD_now",1) 
</drac2>
-f "SD: {{SD_now}} HD: {{HD_now}} HP: {{HP_now}} AS: {{AS_now}} ID: {{ID_now}} WD: {{WD_now}}"

# show stats
!alias ss embed
-f "SD: {{SD_now}} HD: {{HD_now}} HP: {{HP_now}} AS: {{AS_now}} ID: {{ID_now}} WD: {{WD_now}}"

#long rest
!alias lr embed
<drac2>
set_uvar("SD_now",5)
set_uvar("HD_now",11)
set_uvar("AS_now",1)
set_uvar("ID_now",1)
set_uvar("WD_now",1)
</drac2>
-title "takes a long reset"
-f "SD: {{SD_now}} HD: {{HD_now}} HP: {{HP_now}} AS: {{AS_now}} ID: {{ID_now}} WD: {{WD_now}}"

# short rest
!alias sr embed
<drac2>
set_uvar("SD_now",5)
set_uvar("AS_now",1)
set_uvar("ID_now",1)
set_uvar("WD_now",1)
</drac2>
-title "takes a short reset"
-f "SD: {{SD_now}} HD: {{HD_now}} HP: {{HP_now}} AS: {{AS_now}} ID: {{ID_now}} WD: {{WD_now}}"

#attack: atk [adv|dis] [gw]
!alias atk embed
<drac2>
bonus = "+ 10"
myroll = "1d20"
what = "his halberd"
does = "swings"
how = "casually"
adv = ""
thumb = ""
if "adv" in &ARGS&:
    myroll = "2d20kh1"
    adv = " using superior advantage"
elif "dis" in &ARGS&:
    myroll = "2d20kl1"
    adv = ", but at disadvantage"
if "gw" in &ARGS&:
    bonus = "+ 5"
    does = "brutally thrusts"
    how = "with great power"
    set_uvar("GWA", "yes")
else:
    set_uvar("GWA", "no")
if bless == "on":
    myroll = myroll + "+d4"
    how = "with divine guidance"
    if "gw" in &ARGS&:
        how = "with divine guidance _and_ greatness"
myroll = myroll + bonus
set("attack", vroll(myroll))
set_uvar("critical_status",attack.result.crit)
set_uvar("attack_total", attack.total)
msg = "Roll: " + attack.full
if attack.result.crit == 1:
    msg = "Critical Hit!\n__YOP!__|" + msg
    thumb = "https://i.pinimg.com/736x/58/31/a9/5831a90f6dab4a46bd495250f37f4d5b--conan-the-barbarian-movie-arnold-schwarzenegger.jpg"
if attack.result.crit == 2:
    msg = "Fumble!\noh no.|" + msg
    fumble = vroll("1d20")
    msg = msg + "\nFumble Check: " + fumble.full
    if fumble.total > 0:
        msg = msg + "\nOh crap!"
    else:
        msg = msg + "\nThat was a close one!"
</drac2>
-title "{{does}} {{what}} {{how}}{{adv}} for {{attack.total}}" -f "{{msg}}" -thumb "{{thumb}}"

!alias hit embed
<drac2>
myroll = "d10"
bonus = "+6"
if "pm" in &ARGS&:
    myroll = "d4"
if critical_status == "CritType.CRIT":
    myroll = "2" + myroll
if GWA == "yes":
    bonus = "+16"
_damage = vroll(myroll + bonus)
total = _damage.total
adj = "for"
if total >= 20:
    adj = "for a massive"
elif total >= 15:
    adj = "for a decent"
elif total < 8:
    adj = "for a meager"
set_uvar("damage", total)
</drac2>
-title "hits {{adj}} {{total}} HP" -f "Roll: {{_damage}}"

!alias bless embed
<drac2>
if "%1%" == "off":
    set_uvar("bless","off")
    status = "nolonger blessed. :disappointed:"
else:
    set_uvar("bless","on")
    status = "now blessed! :angel:"
</drac2>
-title "is {{status}}" 

!alias sav embed
<drac2>
stats = load_json(stats)
stat = "%1%"
modifier = floor((stats.%1% - 10)/2)
if stat == "str":
    modifier = modifier + stats.proficiency
if stat == "con":
    modifier = modifier + stats.proficiency
myroll = "d20"
if "%2%" == "adv":
    myroll = "2d20kh1"
elif "%2%" == "dis":
    myroll = "2d20kl1"
if bless == "on":
    myroll = myroll + "+d4"
myroll = myroll + "+" + str(modifier)
save = vroll(myroll)
</drac2>
-title "Saving Throw" -f "{{stat}} based:|{{save}}"

!alias indom embed
<drac2>
ID = int(ID_now)
if ID > 0:
    set_uvar("ID_now", int(ID_now) - 1)
    msg = "appears indominable and may reroll his saving throw"
else:
    msg = "sadly looks to his feet and accepts his fate"
</drac2>
-title "{{msg}}"

!alias hd embed
<drac2>
hit_die = int(HD_now)
if hit_die > 0:
    stats = load_json(stats)
    was = int(HP_now)
    r = vroll("1d10+11")
    healed = r.total
    set_uvar("HD_now", hit_die - 1)
    set_uvar("HP_now", min(stats.hp, was + r.total))
    msg = "HD remaining: " + HD_now
    msg = msg + "\nHP was: " + str(was)
    msg = msg + "\nadding: " +  str(r)
    msg = msg + "\nHP now: " + HP_now
else:
    msg = "has used all his hit die"
</drac2>
-title "uses a hit-die" -f "{{msg}}"

!alias heal embed
<drac2>
stats = load_json(stats)
gain = %1%
msg = "is healed for " + str(gain)
val = int(HP_now) + gain
set_uvar("HP_now", min(stats.hp, val))
</drac2>
-title "{{msg}}" -f "HP: {{HP_now}}"

!alias hurt embed
<drac2>
stats = load_json(stats)
gain = %1%
msg = "is hit for " + str(gain)
val = int(HP_now) - gain
set_uvar("HP_now", val)
</drac2>
-title "{{msg}}" -f "HP: {{HP_now}}"

!alias wind embed
<drac2>
WD = int(WD_now)
if WD > 0:
    stats = load_json(stats)
    r = vroll("1d10+11")
    val = int(HP_now) + r.total
    set_uvar("WD_now", 0)
    set_uvar("HP_now", min(stats.hp,val))
    msg = "has a 2nd wind: " + r.full
else:
    msg = "has the wind knocked out of him"
</drac2>
-title "{{msg}}" -f "HP: {{HP_now}}"

!alias prec embed
<drac2>
SD = int(SD_now)
if SD > 0:
    result = vroll("1d10")
    SD = SD - 1
else:
    result = vroll("0d10")
set_uvar("SD_now",SD_now - 1)
total = result.total + int(attack_total)
</drac2>
-f "Precision Strike|rolled: {{result}}" -f "Total Attack:|{{attack_total}} + {{result.total}} = {{total}}" -f "SD remaining: {{SD_now}}"
-thumb "https://marketingepic.com/wp-content/uploads/2015/04/bullseye.jpg"

!alias sd embed
<drac2>
SD = int(SD_now)
if SD > 0:
    result = vroll("1d10")
else:
    result = vroll("0d10")
set_uvar("SD_now",SD-1)
total = result.total + int(damage)
</drac2>
-f "Superiority Die|rolled: {{result}}" -f "Total Damage:|{{damage}} + {{result.total}} = {{total}}"
-f "SD Remaining: {{SD_now}}"

!alias ball embed
<drac2>
eight_ball = [
    'It is certain',
    'Without a doubt',
    'You may rely on it',
    'Yes definitely',
    'It is decidedly so',
    'As I see it, yes',
    'Most likely',
    'Yes',
    'Outlook good',
    'Signs point to yes',
    'Reply hazy try again',
    'Better not tell you now',
    'Ask again later',
    'Cannot predict now',
    'Concentrate and ask again',
    'Don’t count on it',
    'Outlook not so good',
    'My sources say no',
    'Very doubtful',
    'My reply is no'
    ]
val = roll("1d20-1")
msg = eight_ball[val]
question = %*%
</drac2>
-title "asks the gods, \"{{question}}\"" -f "8 Ball says:|{{msg}}" -thumb "http://appinventor.mit.edu/explore/sites/all/files/Teach/media/image_8_ball.jpg"

!alias ini embed
<drac2>
ini = vroll("d20")
says = [
    'This is where we fight! This is where they die!',
    'Come on, you sons of bitches, do you want to live forever?',
    'By the power of Greyskull ... I have the powerrr!!!',
    'Nothing is over till we decide it is! Was it over when the Germans bombed Pearl Harbor? Hell no!',
    'Tulta munille!',
    'Carthago delenda est!',
    'I am the Love Angel, I am Wedding Peach, and I am very angry with you!',
    'Today is a good day to die!',
    'Remember the Alamo',
    'Go Gators!',
    'Liberty or Death',
    'Go fuck yourself',
    'Yawp!',
    'Oorah',
    'Tyr!',
    'We shall have blood this day',
    'Huzzah!',
    'I will be your murderer today, enjoy your death',
    'All your base are belong to us',
    'There is no cure for stupid',
    'There are few problems in this world that cannot be solved by a swift roundhouse kick to the face. In fact, there are none.',
    ]
val = roll("1d" + str(len(says)) + "-1")
msg = says[val]
</drac2>
-title "cries, \"{{msg}}\"" -f "and has initiative: {{ini}}"
