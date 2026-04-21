---
source: notion
notion_page_id: 32000ca3-2bce-80da-94f6-c0faa5d9ec1f
notion_url: https://www.notion.so/Call-Felipe-32000ca32bce80da94f6c0faa5d9ec1f
title: "Call Felipe"
created: 2026-03-11T20:00:00.000Z
edited: 2026-03-11T21:01:00.000Z
empresa: generic
---

# Call Felipe

> [bloco não-suportado: transcription]



### Current Deployment Mix: Copper vs. Optical

- Intra-rack connectivity: 70-80% copper (passive or active), 20-30% optical  

- Inter-rack connectivity: The ratio inverses - approximately 70-80% optical dominates due to distance and bandwidth requirements   

- This pattern is fairly consistent across the industry, with some variation in large AI training clusters that may adopt optical more aggressively 

### Connectivity Hierarchy in AI Data Centers

- Chip-to-chip communication (GPU to GPU, GPU to CPU): Predominantly 100% copper 

- Scale-up (intra-rack): Majority still copper due to cost effectiveness and reliability 

- Scale-out (inter-rack): All optical because of reach requirements and speed 

- Scale-across (data center to data center): 100% optical 

- Rule of thumb: "If copper works, use copper wherever it works until it doesn't work, then use optics" 

### Cost and Reliability Comparisons

- Optical transceivers are approximately 10x more expensive than copper 

- Optical is also roughly 10x less reliable than copper  

- Copper remains the baseline for reliability - critical for GPU-to-GPU communication where failures could mean millions of dollars lost and full restarts 

- Total cost of ownership (TCO) impact: Interconnects currently account for roughly 5% of total system cost, but this is increasing toward 10% or more in the near future   

- When considering full TCO (not just cables), the cost difference compresses to approximately 2-5x more expensive for optical  

### Physical and Technical Limitations of Copper

- At 200 Gbps per lane speeds, copper reach is limited to approximately 2 meters 

- At 400 Gbps per lane, copper reach will likely be less than 1 meter 

- Even intra-rack connectivity becomes challenging at these higher speeds  

- Signal integrity, power consumption, and reach constraints become more pronounced as lane speeds increase toward 800G and 1.6T   

- Industry consensus: "Don't bet against copper" - copper has consistently exceeded predictions of its demise for decades 

### Active Cable Technologies Comparison

- ACC (Active Copper Cable): Lowest power consumption, most limited reach (~2-3 meters at 1.6T) 

- AEC (Active Electrical Cable): Medium power consumption, reach of about 5 meters 

- AOC (Active Optical Cable): Highest power consumption, longest reach (10-100+ meters) 

### Power Consumption and Thermal Considerations

- Active electrical cables (AECs) consume more power per link due to electrical signal conditioning 

- At higher speeds, AECs generate more heat in already dense AI racks, potentially approaching thermal limits  

- Optical transceivers are approaching 30 watts per port or more for newer generations 

- Many AI environments are already operating much closer to thermal limits than traditional cloud racks 

- Dense GPU clusters combining high-power GPUs with 800G connectivity are pushing thermal margins tighter 

### Cooling and Rack Design Evolution

- Liquid cooling is becoming the new norm due to high power density  

- Liquid cooling is being applied not just to GPU trays but also to switch trays 

- Rack disaggregation is emerging as a trend to manage power density limits - moving GPUs further from switches  

- Rack disaggregation increases reach requirements, potentially forcing more optical technology adoption  

- Data center facilities are hitting power limits from local utilities - US government action may be needed to resolve this constraint 

### Reliability and Failure Modes

- Reliability ranking (most to least reliable): Passive copper > Active copper > Optical 

- Typical failure mode is network degradation rather than complete compute failure 

- Link flaps (links going down and quickly coming back up) can halt GPU training and require restarting from checkpoints 

- Link flaps occur more often with optical than copper 

- Optical transceiver failure modes include: contamination, laser/photodiode component failures, and firmware bugs  

- Google publicly identified firmware failures as one of the top three failure modes for optical transceivers 

- Estimated link flap occurrence during training: less than 5% 

- Operators prefer copper from a handling perspective - optical is susceptible to contamination, handling issues, and misuse on the data center floor 

### Vendor Positioning and Competitive Landscape

- Credo: Stronger presence in copper (passive and active), though expanding into optical transceivers - key opportunity is in power efficiency and signal integrity for electrical connectivity  

- Lumentum: Focus on optical components and cost scaling - needs to deliver higher speeds with good reliability and lower power consumption 

- Coherent: Advantage in manufacturing and photonics integration - positioned to scale high-volume production of photonic components 

- Both Lumentum and Coherent have vertically integrated portfolios from optical components (lasers) to transceivers and optical circuit switching products 

- NVIDIA invested $2 billion in both Lumentum and Coherent to lock in optical supply chain 

- Google uses optical circuit switching technology, with both Lumentum and Coherent supplying products 

### Co-Packaged Optics (CPO) Outlook

- Growing interest as speeds move toward higher lane speeds and eventually 1.6T 

- Main motivation: improving power efficiency and signal integrity by bringing optical interface closer to switching silicon 

- Adoption will take time due to serviceability and operational reliability concerns  

- Pluggable transceivers remain easier to replace and manage 

- Both models expected to coexist in the near term 

- NVIDIA is pushing hard on co-packaged optics with Lumentum as a known partner 

- Industry consensus: Co-packaged optics will increase gradually, not overnight - pluggables will continue to dominate for coming years 

- Barriers to adoption: proving reliability comparable to pluggables, gaining customer confidence, finding early adopters willing to take the risk  

### Future Projections

- Next generation products will likely still use mostly copper for scale-up/intra-rack connectivity  

- Two generations beyond next-gen is difficult to predict - depends on copper industry progress with new packaging technologies and connectors 

- Optical adoption will expand as speeds increase, but copper won't disappear entirely for very short-reach connections    

- The boundary where copper is practical keeps moving inward (shorter distances) as speeds increase 

- Interconnect costs as percentage of total system cost are steadily increasing from current ~5% toward 10% or more, driven by the need to interconnect larger numbers of GPUs (500K to 1M+)  







Look for copper versus optical connectivity among a variety of different players here. Thank you very much to the panelists, joined by a project manager of data centers at AWS, Ioeb, as well as a network architect at Dell Technologies, GN. To begin, I want to...

deployment mix between copper and optical cables for both intra-rack and inter-rack connectivity and adoption trends especially as we transition to 1.6T here.

So Ayub, let's start with you first here. First question for you here is, you know, in companies like major cloud providers and OEMs, how is the typical mix between passive copper, active copper, and optical How is that evolving as we move from 400G to 800G and now really starting into 1.6 terabyte territory in AI and Cloud data centers?

So that's actually a very good question to start with. Let's say from what I have seen in hyperscale deployment, covers still dominate inside the rack, mainly because it's lower cost and easier to manage operationally. So let's say most of the GPU to GPU server are to switch. connections within the rack are still using passive or active cover cables. When we are talking about, now once you move beyond let's say the rack connecting roads or let's say a scaling clusters, optical here becomes the preferred option because it really supports longer distances and higher bandwidth.

Now as the industry is moving, so, so Let me elaborate on this also more like if you look at directionally, inside the rack might be something like 70-80% copper and the rest optical, depending on the architecture. When we are talking about interact, it's almost the opposite. Optical dominates because it supports higher bandwidth and longer reach. So as we move, let's say, toward 800G and eventually 1.6 Tera networking, here optical adoption will likely expand, you know, further.

But Kepa also will still have a role, you know, for very short reach connections. Interesting.

Okay. So if I understood correctly here, you're saying active or passive copper still is maybe 70 to 80% in racks. But then you said when you move to beyond the rack, that kind of inverses where now it's 70 to 80% optical. Is that correct? Did my understanding correct there?

That's absolutely correct. Absolutely right.

Got it, got it, okay. And then I guess just to clarify a little bit more here, within the racks that we have out there today, how do you think How many, or I guess within the architecture that we have today, is that range that you gave 70 to 80% mostly copper, is that across the industry or is that... shift around depending on the verticals or different kind of infrastructures that you see. Maybe you can expand on that a little bit.

So the range is actually consistent with what we see across the environment. Like let's talk about inside the rack, most deployments are still heavily copper. Now we have like passive also passive DAC for the very short links and active KEPR when signal integrity becomes more challenging, you know, at higher speeds. So yeah, seeing something like 70-80% KEPR inside the rack is pretty typical. Now where it starts to shift is when you once you move beyond the rack you know at that point yeah optical becomes the dominant choice because of the distance and bandwidth you know requirement.

Now definitely there can be some variation you know depending on the workload or or as you said like architecture like for example this like large AI training clusters may adopt like optical a bit more aggressively you know but broadly speaking that cap or inside back and optical between racks pattern is fairly consistent you know across the rack or sorry across the industry Okay, across workloads and architecture, largely similar.

That's correct. Got it, got it. Okay, great, great. Thank you for clarifying that, Ayub. And then, Jian, anything else to add here from your perspective?

AI data center. So there is a chip to chip communication and there is a so-called scale up interconnects and there is a scale out interconnects and then there is something called the scale across that's between so a chip to chip is is basically gpu to gpu gpu to cpu and the second one scale up is means broadly speaking is inside inside the rack uh intra rack and then scale out means interact between the racks and scale across means means between data centers to data centers broadly speaking so uh chip to chip communication is is predominantly basically 100% copper and scale up that intro the intro rack that that's basically majority is still copper and the reason is obvious is for cost copper is cost effective and very reliable compared to optics and that's the main reason if copper works usually there is like a rule of thumb if copper works use copper wherever it works until doesn't work and I use optics.

So scale out, like interact is basically all optics because of the reach requirement and also speed and scale across that means between data center to data center is 100% optical.

Okay, got it, got it. That's very helpful. And then I guess, Jan, any rules of thumb in your experience of, How to think about cost here generally? I know you mentioned copper is generally more cost effective and very reliable compared to optics. What does that end up looking like? Is optics two to three times more expensive than copper in general? How do you kind of frame that?

Yeah, yeah. So I think roughly speaking, optics is 10 times more expensive than copper and also 10 times less reliable than copper. You can think about that way. Roughly speaking, yeah.

Got it. Got it. Okay. So roughly 10 times more expensive and 10 times less reliable. Interesting. Okay. Makes sense. And then, Jang, one other question for you here. So I guess from your expert view, as we think about the next, let's say, two to three architecture refresh cycles, right? I know that takes a little bit of time, but over the next two to three refresh cycles, what do you expect like a standard, you know 72 GPU or a larger AI cluster to look like in terms of the percentage of ports on passive active copper and then optical transceivers inside of the rack versus between racks the infrared how do you see that percentage shifting there maybe yeah so that's a little bit difficult question to answer I think it's really depends on the typology and architecture each hyperscaler chooses to use.

But basically for the next generation of speed requirement and copper won't transmit anything longer than roughly two meters, I would say, at the 200 gigabit per second per lane technology generation. So it won't go beyond anything to the three meters. So that basically means And you can only use it inside the rack. And going even beyond like 400 gigabit per second per lane, and copper reach probably is less than one meter.

And even reaching inside the rack can be quite challenging. And if copper can make it work at all. So now it is a very challenging work industry. Realize at the next generation speed, copper is facing significant challenge.

The copper people will make it work one way or another in a matter of time. There are promising results coming out from industry that indicate it will work still, but it's a question of how long and whether that meets the requirement of the typology, the hyperscaler needs. So that basically means it's quite evident that copper is facing a war here. I see. technologies, for example, micro LED technologies and/or some kind of new RF technologies that can extend the reach of copper.

So there are different technologies people are looking into, different startups and etc. So try to resolve this, the so-called scale up domain, because we do see that copper is becoming very, very challenging now. It's facing a war.

Interesting, interesting.

And then just one more follow-up.

Yeah, yeah, that's what I was going to just ask in terms of, you know, like you said, the scale up, the intra-rack. If you had to put a rough estimate on it, is that something you're able to do? Just of how much percentage would be copper versus optical?

Yeah, so I think take a media example and look, I think for the Next generation product they will still use copper for for most of the steel up is probably mostly copper steel and for the like maybe two generation beyond it is it is difficult to predict. Depending on how the copper industry progresses, it's really hard to predict at this point. If copper still works, somehow people figure out using new packaging technology, new connectors, and etc.

If copper works, people will still choose to use copper just because it's reliable and cheap.

Got it, got it. Okay, so for next-gen, probably still similar percentages today. For the gen after that and beyond that, that's difficult to say. But if the copper technology advances, you predict we'll still continue to use that because of the reliability and the cost. Yeah.

Yeah, basically I think you can say it safely that don't bet against copper. And people have been seeing optics taking over copper for decades and copper are still working very reliably and just very well.

Okay, great, great. Yes, I want to dive into that a little bit more. But before we do that, thank you for that, Jan, by the way. Ayub, anything else to add here from your view?

So actually Jane made a good point about the physical limits. Yes, in practice once you get beyond like roughly a couple of meters, yeah, copper becomes much harder to maintain, you know, especially from a signal integrity and power perspective, especially as speeds move toward like, you know, 800 G and eventually 1.6 Tera. So The next AI cluster is refresh cycle. I would expect also both passive and active electrical cables to remain primarily as in rack solutions.

As Jane said, for very short lengths like GPU to GPU, GPU to top of rack switch, cable is still attractive because it's simpler and cheaper. But yeah, where the shift really happens is when you scale beyond the rack. Extend to take you know over because it handles distance thermal efficiency much better, you know And yes, actually, I completely agree. That's why we're seeing more discussion around things like co-packaged optics or other even optical integration approaches because the industry is essentially trying to solve the same problem, like how to move massive amounts of data between, let's say, accelerators without running into a power limitation or a signal limitation.

Yeah, yeah. No, it makes sense. I guess a question for you here, Ayob. So I guess when we think about today and even like the next generation of lane speeds, like we've been talking about here, you know, 800G, 1.6T, where do you see copper maybe topping out or the limits of it in terms of reach and speed or deployments? I know you talked about there's other new technologies, co-packaging, all these other things.

But do you see a point where maybe there is a limit and we have no choice but to go optics only? Do you see a space where that becomes the case? So...

As long as KEPR is working, we're going to stick with KEPR. So KEPR starts, let's say, KEPR starts hitting real limits as we move into the 800G generation. And especially toward 1.6TB, because it's going to be mainly a combination of signal integrity, reach, power efficiency, So as you said, the land speeds increases. We need to maintain like clean signal over Kepa because it's going to be much harder beyond very short distances.

So what we are seeing is that Kepler can still work well for very short N-Rack connections. maybe around a metre or two. Particularly with active electrical cables, you know, but once you push beyond that or try to scale higher bandwidth fabrics, optics here becomes like the more practical solution. So, I wouldn't say Kebber disappears, you know, but it's... usable reach, keeps shrinking as speed increases.

Interesting. Yeah, that naturally pushes more of the connectivity stack toward optics, especially as we move into the next generation of AI clusters.

And so just to clarify, do you see any of these other technologies kind of like Jan was describing here as potentially being able to ensure copper stays in the mix? Or do you kind of believe like it's only a matter of time until we become an optics-only world? You know, once we just kind of normalize and reach certain lane speeds, Are we done with copper or do you still see a pathway here for copper?

Maybe you could expand on that a little bit.

Yeah, so from what from actually what we're seeing today, I don't think again, cable disappears like entirely, especially for very short reach connection, you know, like inside the rack. Technology is Technology is actually like improved active electrical cables and better so this, you know, continue to push the limits like a bit farther. The challenge is that as lane speeds move toward like 800 G and eventually 1.6 Tera, here the physical limitation of cover become more pronounced, you know, like we have the signal integrity becomes harder to maintain.

We have the poor consumption. increases, the reach also tends to shrink. So actually what used to work like over a few meters might only work over a meter, you know, or so, you know, like at higher speeds. So yeah, because of that, the boundary where copper, let's say, is practical keeps moving inward. like inside the racket. It still has a role, but once you move beyond that, again, optics becomes the more scalable solution.

Got it. When we're talking about co-packaged optics or even other optical integration approaches, the industry is essentially trying to keep up with the bandwidth demand of AI clusters. And definitely optics provide a more efficient way. Ah. So I would say the long-term direction isn't that Kepard disappears overnight, but the optics like he gradually takes over more of the interconnect.

Interesting. Okay. Great. Great. Thank you for that. That's helpful. And then, Jian, slightly related, but slightly different question here. You know, when you think about data center operators and as they design some of these new AI clusters, I guess from your view, how are they comparing operations? total cost of ownership of short-reach optical versus active copper considering that you know the equipment cost the power the cooling rack density right operational complexity how do they think about total cost of ownership when they're comparing these two Okay.

Yeah, that's a good question. So for the copper, and there are a few technologies that push beyond the copper for example there is a acc which is time for out activeYeah. copper cable and AEC active electrical cable and these two can it extends the reach of the copper, but that's a compromise of increased cost and increased power consumption. And then if you look at this intercept, so there will be an intercept that this copper becomes harder and harder to push beyond a certain speed limit, and then you pay more cost and you pay more power, and that will be an interception between this active copper cable with the optics.

technology. So and then in terms of the cost and the power consumption. But one thing is very clear is that as of today the optics Copper is still the baseline for reliability. It's still the most reliable technology compared to optics. And optics is roughly 10x worse in reliability, if not more. So only if optics can reduce reliability, sorry, improve the reliability by 10x, and then I think it can comfortably compete with copper.

Otherwise people will likely still choose to use copper and just because it's more reliable. And especially for the inter-rack, sorry, the intra-rack interconnects and reliability is key. And because you don't want this GPU to GPU communication to break down. Otherwise that means like millions of dollars lost. Everything has to restart again. So it needs to be extremely reliable. And copper is still a good medium for meeting that requirement.

Yeah, so--Interesting. Yeah.

Okay, so I was just gonna ask, so, Yes, as you mentioned, copper is 10 times less expensive, 10 times more reliable. But I guess even considering the cost of equipment, the power and the cooling, the rack density, right, all the operations, even considering all that, you're saying it is still more affordable than optical.

Yes, I would say so. That's right, yes.

Okay, got it. And then if you had to kind of provide a framework of when you consider total cost of ownership, is that I know earlier we talked about 10 times more expensive for optical. Is that in general? Is that just for the cables? Or is that when you consider total cost of ownership? Or does that total cost of ownership maybe compress and only becomes two to three times more expensive? when you account for total cost of ownership, what does that expense look like?

Yeah, good question. So I think what I'm saying is in generally that that's for the cable itself. Yeah, so then the transceiver, I'm mainly talking about the transceiver itself. If you look at the cabling, there is also a fiber cost too if you go to optical technology. So that fiber also is not cheap. So that's also add to your total cost ownership. Also all those servers and everything like storage and compute and everything is part of that total cost of ownership.

So yeah, one thing is that even from the operational perspective and most of the data centers who work in the technicians who work in the data center and then they will prefer copper versus optics because it's very susceptible to contamination. handling and misuse which often happen inside data center floor and you will have worse system performance compared to copper topology. So copper is just very easy to plug in and it works fine.

Got it, got it. Okay. And then any figure that you feel comfortable with on that total cost of ownership? I know you said that 10 times is just for the cable itself, but for total cost of ownership, is it also just 10 times more expensive or would that be slightly less?

Um... Hmm. I think that will probably study less because interconnect is part of only a portion of the whole system cost. So maybe account for 10 to 20% maximum of the total cost. So then if you look at that, the total cost of ownership will be less, much less than what I mentioned 10 times.

Any estimation of what that might be or too hard to say? And...

I don't really have a number. No, that's fair.

Yeah, just wanted to see if instead of 10 times, it's five times or five to seven times or something like that, right? If there is a range, but maybe it's difficult to say.

Actually, I would assume it's between two to five percent range, you know, of TCO because the majority of the costs are still in GPUs, which is power infrastructure. So that's why I would assume like it's between two and five. That's actually my assumption.

Two to five times as expensive when you account for total percent. Yeah, yeah, yeah. for total cost of ownership. Yes.

Got it.

That number is increasing.

I think you're right, 5% is current kind of the percentage how much this interconnect technology cost overall and then that number is increasing to steadily to maybe close to 10% in the near future or even more than that.

And why do you say that, Jian?

Just because of the demand and the increased--Yeah, so because of the cost for each generation and these transceivers are very costly. And for 1.6T, 3.2T, and also because of the, in order to integrate more GPUs and then the interconnection becoming the new bottleneck. It's not the compute that's the bottleneck. and more transceivers and fibers to interconnect a half a million GPU or even a million GPU up to.

So that interconnection will account for even a bigger and bigger portion of the total system cost.

Got it, got it, okay. So maybe two to five-ish today, but increasing to 10 or more in the near future. Yes. Got it, got it. Okay. Ayub, any final thoughts on that before we move on to another?

No, I think that's the reason of the observation, actually. Because, yeah, one of the things that I would think about, that one reason, like the gap can widen, you know, again, as the expert said, is that we move to higher speeds, like 800 G, eventually 1.6 Gera. So, yes, the optical transceivers themselves becomes much more complex, expensive you know so because you're dealing with uh like more advanced dsps lasers packaging similar requirements so the module cost yeah naturally goes up Yeah, at the same time, you have the copper, you know, which is also getting more complex, especially when we are talking about active electrical cables, you know, AECs.

But it's still, let's say, like generally simpler than optics, like from a component standpoint.

Sure. No, it makes sense. Makes sense. Okay, great. Well, let's keep moving here. I want to get through a few more questions. for this next one as well. Let's talk a little bit about AEC versus AOC power efficiency and the thermal load of active copper cables on AI racks. So I hope the question here is, in dense AI racks that are running 800G today and maybe evaluating 1.6T, How does the typical power consumption and heat output of the active electrical cables compare to active optical cables on a per port basis?

Like how, what's the difference there and do facilities ever come close to hitting some sort of a power or thermal limit here?

AEC versus or compared to what, sorry?

Let's for this one, just overall active optical versus active electrical. Oh, gotcha.

Yeah. That's actually a very good question. Now from a thermal standpoint, That's becoming a bigger factor, especially when we're talking about rack densities increasing. For the AECs, Active Electrical Capables, you know, they tend to consume more power per link because They rely on electric and signal conditioning. As you said, like as speeds move toward 800 G and potentially 1.6 T, that power consumption can translate directly into heat, you know, like inside already dense AI racks.

But with optical connectivity, actually, a lot of signal transmission happens, you know, through the optical. So... Also the transceivers like themselves, they still consume power. So the thermal load per meter of link can be, I believe it can be more manageable, you know, especially as distances increases. So like in my point of view in very dense AI racks thermal efficiency becomes Yes, an important consideration.

If copper links require more signal boosting to have higher speeds or maintain integrity, the heat profile can start favoring optical solutions. Hmm. Does that make sense?

Yes, yes. You start maybe reaching a sort of thermal limit with the active copper, it sounds like, and maybe it becomes more favorable to go the optical route.

That's correct. That's absolutely right. Because... Ah. Actually, that's really where the challenge starts showing up. AAC needs more signal conditioning. They need like over, I mean, over copper, you know, over... that additional electronics generates more heat inside the rack So, especially when we are talking about very dense AI racks, where you already have GPUs running at extremely high power levels.

You can start approaching thermal limits with AACs very quickly. So the power and heat from those cables become a real design concentration. And in my perspective, that's one reason optics becomes more attractive beyond shortest lengths. Because even though optical transceivers... Like consume power. But the overall thermal profile can scale better, especially at higher speeds and longer reach. And definitely, especially in high density AI clusters.

Yeah. So I guess I have one clarification here. So given that, given what you just said there, I guess when you think about all these different facilities that are out there that are running very dense AI racks, how close are most of them to reaching this sort of thermal limits or this interconnect power limit. from your view?

How close? Like, Like I do not have really a specific answer to this, but it really depends on the facility design, you know, like in many AI environment. They are already operating much closer to thermal limits than traditional cloud racks. Because when you combine high power GPUs with 800G connectivity and more active components in the rack, I can't. Like thermal margin gets tighter pretty quickly, you know, so I wouldn't say every site is at the limit today, you know, but a lot of operators are cleanly designing much closer to the edge than they used to.

And that's exactly why thermal efficiency is really becoming a bigger factor, you know, especially in cover versus optics like discussions.

Right, right. Makes sense. Makes sense. Okay, great. Great. Thank you for that, Ayub. And then, Jian, similar type of question, but slightly different for you as well. I guess when you think about some of these high density GPU cluster designs, how are all these thermal limits, power limits, everything, especially as we go from 800G to 1.6T speeds? How are those constraints, changing or shifting the way that operators think about laying out their racks or their rows and pods?

How do they think about those design choices?

Yeah. So, uh... Just, yeah, before answering that, and I just have one something to add on like your previous. So if you compare this ACC, AEC and AOC, AOC, Active Optical Cable. So basically ACC has the least amount of power consumption. and then followed by AEC and then AOC has the highest power consumption. But, so basically ACC maybe, but the reach is the reverse. So ACC having the least power consumption, it has the most limited reach, maybe at 1.6T generation, probably two three meters something like that and AEC has reached about maybe five meter roughly and AOC will have reached beyond 10 meter or up to a hundred meter.

So that's by design. So really depends on how the system architect design these racks so then people can choose different technology accordingly. So back to your answer. Sorry about this design and cooling facility and etc. So, there is an air cooling technology and then people in the entire industry is moving very quickly to liquid cooling. And liquid cooling is not just on the GPU trays, but also on the switch tray.

So liquid cooling is becoming a new norm right now, just because of the power consumption and power density within the racks is so high. And also this optical transceiver consuming so much power quickly approach 30 watt per port or even more than 30 watt for the newer generation. So then that basically breaks the limit of air cooling capability. So you have to move to liquid cooling. for the future generation and to make it more basically future proof.

So everybody's moving to liquid cooling. And even with the liquid cooling, there is a new trend because for the new, for this, every generation GPU, speed doubles and power consumption also goes up. And at the same time, this transceiver is consuming more and more power. So your power density within the rack, it becomes so high, the physical limit of how much power you can deliver per rack. So people are talking about this rack disaggregation.

So that's another option the system architectures are looking into to disaggregate the racks rather than putting everything in one rack and then you move GPU to GPU further away and from the switches and etc. So that also means That also links to the question of when optics will replace copper. Because as you flag it, this aggregate is rags, that means the reach requirement will be more. So two meters of copper reach isn't enough to meet that requirement.

People, system architect will be forced to think of optical technologies in order to meet the reach requirement.

Got it. Got it. Okay. Great. Great. So then a follow-up here for you, Jiang. So given that, what does that generally imply for companies like Acredo, like Illumentum, right? Coherent Labs, the companies that we're talking about here, what does that imply for companies like that where, you know, what are some of the characteristics of the providers that in your view will be better positioned to take advantage All these changes, right?

The liquid cooling, the changes in architecture, the length of how far you can go, right? Like, what are some of the characteristics of the companies that you think will be better positioned to take advantage of all these things and why?

Yeah, so I think for Lumentum and Coherent, they have pretty similar product portfolio and they're more of an optical focus company. They have a complete portfolio of optical components from lasers and modulators and photodials and etc. to transceiver modules. And for a company like Credo, traditionally they have a stronger presence in copper. Whether it's passive copper or active copper. So even though they are also getting into the optical transceiver business quite quickly, I think most of the revenue is probably coming from the copper side of the technology product.

I think which company will be better positioned and it is I'm not sure if I'm well equipped to answer that question. So basically, optical technology is becoming... So for multiple technology requirements, or interconnect requirement, like whether it's scale out or scale across, and then we will have more and more optical technology needed. And because of the demand, it is increasing. And at the same time, as we've been Nothing and optics will likely intercept with copper for for the two generations ahead Whether is through the form of co-packaged or still pluggable that that percentage will continue rising so then this optical companies will will will be Seeing more and more demand I would I would predict and And also at the same time, we're just talking about optical transceivers.

And you know that as public information, Google uses optical circuit switching technology for their data centers. And both Lumentum and Coherent have optical circuit switch product as well. So that also accounts for quite big, in the coming years, quite big part of the revenue sources, revenue income as well. That's beyond the transceiver product. And at the same time, Amedia is pushing very hard on co-packaged optics and Lumentum is a known partner of Amedia, I think coherent as well.

Amedia recently invested $2 billion on each company and then the main motive behind is that Amedia is seeing this huge demand of optical technology and they want to lock in the supply chain. against other competitors. So both Lumentum and Coherent are very well positioned because they have a vertically integrated portfolio from optical components, lasers especially, all the way to transceivers and even optical circuit switching products.

Got it, got it, great, great. No, that's super, super helpful there. Thank you for that. And then Ayub, anything else to add here from your view? Ah.

Yeah, actually if I want to touch each company's like separately, I would say a credo like the key opportunity is really around power efficiency and like signal integrity and their electrical connectivity. Let's say if... If they can reduce power per port while maintaining reach and reliability, actually that directly improves their thermal profile of the rack. And that's where companies like focused on something like advanced service and active electrical cables, which actually can gain also market share.

For Lumentum actually the focus is more on optical component and like cost scaling. So... Thank you. They need optical modules that can support higher speeds with good also reliability and lower power consumption. So if they can improve the efficiency of lasers and some photonic components, that makes also their optical connectivity more attractive like at scale. For Coherent, their advantage is more on the manufacturing and Photonics also integration side.

As we said, as demand for optical connectivity grows, especially in AI infrastructure, here operators need high volume or less reliable supply of photonic components. So yeah, vendors also can scale production. like while improving efficiency. and also performance, you know, can capture more of that demand. So... This is actually my point of view and I think for the co-packaged optics it's likely going to be seeing growing interest especially as we move toward like higher like lane speed eventually to 1.6 because the main motivation is improving power efficiency you know and signal integrity by bringing the you know the optical interface much closer to the switching silicon so if for operators actually reducing power per bit and thermal load you know around the networking ships becomes actually increasingly important so and co-packaged objects can help you know address address this So yeah, I think adoption will probably take time Because operators care about serviceability, they care about operational reliability, which we still do not see it for the co-packaged.

Like today, plugable transceivers are easier to replace and manage, right? Mm-hmm. In the near term, we may see both models co-exist. If power demands keep rising, I believe that co-packaged optics could become more attractive, especially in future architectures.

Interesting, interesting. Okay, makes sense, makes sense. Yeah, so I was just going to ask more about that, but I think you're answering most of it. So, yeah, basically, you expect to see more of a demand and interest in co-package optics. And so, yeah, I guess just you expect to see a greater share of the cost there. Is that accurate? That's accurate. Got it, got it. Okay, makes sense, makes sense.

Okay, great. Well, let's keep moving here. Let's talk a little bit about, you know, we touched on it briefly, but, you know, the reliability and the failure rates of active cables compared to passive copper. So I guess just to get a little bit of more framework around it, you know, across large AI and cloud deployments, what are the typical observed failure rates for passive copper activity? upper and optical modules after a year of operations, let's say.

Is there a rule of thumb or a general kind of failure rate that's observed? And then do those failure rates, you know, do they present themselves more so during GPU training or inference workloads? Or maybe it doesn't matter.

White bread, that white pizza be very stable over time. Now, when we were talking about ActiveCoupler, the failure rates can be slightly higher, you know, because you now have electronics inside the cable, you know, doing signal conditioning. So, let's say over very large AI deployment, we have, as you know, like thousands of links.

So, you will see some failures, definitely, but they are still relatively manageable.

When we are talking about optical links, actually reliability is also quite good, but the failure modes are a bit different. Because issues here can sometimes come from the transceivers themselves or even fiber handles, like connector contamination or module falls, for example. I would say failures usually show up as network links, link errors, or degrade connectivity.

It's not like a complete failure.

So, yeah, it doesn't matter actually whether it was for GPU training or interference. I cannot really give an exact percentage of rates, but if you want to rank it down or break it down, I would say, would be the passive kepler, then active kepler, then optical.

Got it, got it. And then just one brief clarification. Since one of the last things you mentioned here was reliability and the failure modes are different. You said it shows up more in degraded connectivity, but not compute failure. Is that the case across all three?

Or is that just the case with optical? Ah.

No, actually.

I believe that's one for the political, because... Thank you.

Now, if we want to talk about like, generally speaking, generally speaking, it's across all three, you know, like whether it's passive, kepper, or active kepper, or even optical links, because it's... You know the typical failure mode is more about networking degradation. You know it's more than like compute failures. Because if links start failing or showing errors, let's say, it usually appears as reduced bandwidth or packet errors or a dropped link.

And the network fabric like Pre-route traffic. So the GPU themselves typically keep running. So the workload continues, but may experience some performance degradation. So the difference actually across these technologies is mostly in how failure happens. Like when we're talking about passive copper failures, they're relatively rare and usually physical. When we're talking about active copper, can fail at the electronic level.

Optics, the failure is really often tied to transceiver module or fiber interface, like rather than the cable itself. Does that make sense?

Got it. Yep, yep. Makes total sense. Makes total sense. Okay, great, great. Thank you for that, Ayub. And then Jian, anything else to add here from your perspective?

Yeah, I think one thing I would like to add is that there's this concept called the link flap during training. Link flap basically means that some link is down and then quickly come back up again. And whenever that happens, for the large-scale GPU training and it will basically means there will be a certain retraining required and basically it will be halted and then and have to restart again from a certain checkpoint So that will for sure degrade the overall system training efficiency.

So we don't wanna see a link flap to happen. And that link flap, Um, I think often, in my experience, comes from more on the optical side rather than the copper side because copper is much more reliable than optics and optics and that can come from a different failure mode for the optical transceiver so yes and contamination can be one contributing factor and even inside optical transceiver there are laser component photodiode component and those sometimes can have like failure and and the occasional is could also be due to the software side of thing which means that uh in this high advanced optical transceiver module there is also dsp inside sometimes some firmware bugs and those bugs could also cause the more link flaps uh so and different different failure mode can happen uh for the optical transceivers and i don't really know if Do we have any numbers available?

Because a lot of times the hyperscalers keep these numbers not public. Even though they do have such statistics themselves, for sure. I think Google publicly published something last year in one of the optical conferences.

Basically, they saw that a firmware failure one of the top three failure component failure modes that happens with optical transceiver And they didn't say-Link flap is one of the top three, you said, from Google Publish? Not link flap. I'm saying the reasons that cause the hardware failures of this optical transceiver. What's the failure mode for this optical transceiver? So firmware is one of the top three.

Thank you. Got it, got it. Okay, great, great. That's super helpful. And then, Jen, I know you said that a lot of these hyperscalers keep this information private, so we don't have to go there. I guess from your experience, if you had to estimate any sort of link flap percentages and how often that happens during training, is that something you have experience with at a high level here?

And I think that probably not more than a few percent, less than 5%, I would say, roughly.

Got it, got it. Okay, less than 5% during training, and that happens with the optical side, generally speaking. Yeah. Got it, got it. Okay, great, great. Well, we're getting close to time here, so I'll just ask the final question to each of you, which is just any final thoughts to share? Anything else that you think we should have talked about but didn't get a chance to in this call, maybe for a future discussion?

I'll start first with you, Jian, and then we'll wrap up with you, Ayo. But yeah, any final thoughts to share here?

you I think one interesting thing to see is that how the co-packaged optics technology will play a role increasingly. The industry consensus is that it is going to increase but not overnight and it's going to increase slowly, gradually and pluggable will still continue to dominate for the coming years. Um. Yeah, so due to different deployment and serviceability reasons, that's what makes the hyperscalers and customers to adopt such new technology.

So there are a lot of barriers that yet to be resolved.

Got it, got it. Any catalysts you see that might provide more of an impulse to make that increase happen faster?

Yeah, I think one thing is that from the companies who make this and how one they can prove such technology as reliable as the pluggables and that's one thing and to gain more reliability data to gain confidence among the customers. That's one. The other thing is that whoever is going to adopt technology first and who is willing to take this risk. to the customers.

Got it, got it. Hyperscalers and so forth. Yes, that's right. Got it, got it. Okay, great, great. Thank you for that, Jian. And then Ayub, any final thoughts from your end?

Maybe one thing I would add also is that AI clusters As you know, like keep getting larger. So operators are really starting to think about the whole system. It's not just bandwidth, not just power, not just thermal or even reliability and serviceability. You know, it's all start to matter, especially when you're running like thousands of GPUs together. So what actually we're seeing is less about like is a less of single technology replacing night, you know, as Jane said, it's more of practical mix, like cover where it works well, optics where scale and distance requires it, you know, and definitely newer approaches gradually coming into the architecture as the industry keeps pushing, you know, toward higher speeds.

So yeah, that's all for me. Thank you so much for having me on this call.

One thing. Yes, yes. Yes, go ahead. Yeah, so we talk about this power consumption a lot and then the powering of this data center is becoming very critical in the coming years. And the data center facilities is facing a big limit on how much power can they actually get from the local cities or governments. That's basically is hitting a wall and US government needs to act very fast to resolve this power limit.

Definitely, definitely. Okay, great, great. Well, Jan, Ayub, thank you both so much for taking the time to share expertise. So thank you. Thank you.

Take care. Bye-bye. recording The President: It's a beautiful place.

It's a beautiful place. -I'm going to go straight to the cup, yes.

Brazil Let's see a little bit. Dying will be bad. Oh yeah. AirplaneGot the minute thing. Airplane- Got the minute thing.
