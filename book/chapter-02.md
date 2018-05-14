# Neuron

One major reason the brain can be so plastic and learn to do so many different things, is that it is made up of a highly-sculptable form of *silly putty*: billions of individual neurons that are densely interconnected with each other, and capable of shaping what they do by changing these patterns of interconnections. The brain is like a massive LEGO set, where each of the individual pieces is quite simple (like a single LEGO piece), and all the power comes from the nearly infinite ways that these simple pieces can be recombined to do different things.

So the good news for you the student is, the neuron is fundamentally *simple*. Lots of people will try to tell you otherwise, but as you\'ll see as you go through this book, *simple neurons can account for much of what we know about how the brain functions*. So, even though they have a lot of moving parts and you can spend an entire career learning about even just one tiny part of a neuron, we strongly believe that all this complexity is in the service of a very simple overall function.

What is that function? Fundamentally, it is about **detection**. Neurons receive thousands of different input signals from other neurons, looking for specific patterns that are \"meaningful\" to them. A very simple analogy is with a smoke detector, which samples the air and looks for telltale traces of smoke. When these exceed a specified threshold limit, the alarm goes off. Similarly, the neuron has a **threshold** and only sends an \"alarm\" signal to other neurons when it detects something significant enough to cross this threshold. The alarm is called an **action potential** or **spike** and it is the fundamental unit of communication between neurons.

Our goal in this chapter is to understand how the neuron receives input signals from other neurons, integrates them into an overall signal strength that is compared against the threshold, and communicates the result to other neurons. We will see how these processes can be characterized mathematically in computer simulations (summarized in ). In the rest of the book, we will see how this simple overall function of the neuron ultimately enables us to perceive the world, to think, to communicate, and to remember.

**Math warning:** This chapter and the [Learning Mechanisms Chapter](CCNBook/Learning "wikilink") are the only two in the entire book with significant amounts of math (because these two chapters describe in detail the equations for our simulations). We have separated the conceptual from the mathematical content, and those with an aversion to math can get by without understanding all the details. So, don\'t be put off or overwhelmed by the math here!

## Basic Biology of a Neuron as Detector

shows the correspondence between neural biology and the detection functions they serve. **Synapses** are the connection points between **sending neurons** (the ones firing an alarm and sending a signal) and **receiving neurons** (the ones receiving that signal). Most synapses are on **dendrites,** which are the large branching trees (the word \"dendrite\" is derived from the Greek \"dendros,\" meaning tree), which is where the neuron integrates all the input signals. Like tributaries flowing into a major river, all these signals flow into the main dendritic trunk and into the **cell body**, where the final integration of the signal takes place. The thresholding takes place at the very start of the output-end of the neuron, called the **axon** (this starting place is called the **axon hillock** \-- apparently it looks like a little hill or something). The axon also branches widely and is what forms the other side of the synapses onto other neuron\'s dendrites, completing the next chain of communication. And onward it goes.

This is all you need to know about the neuron biology to understand the basic detector functionality: It just receives inputs, integrates them, and decides whether the integrated input is sufficiently strong to trigger an output signal.

There are some additional biological properties regarding the nature of the input signals, which we\'ll see have various implications for neural function, including making the integration process better able to deal with large changes in overall input signal strength. There are at least three major sources of input signals to the neuron:

-   **Excitatory inputs** \-- these are the \"normal\", most prevalent type of input from other neurons (roughly 85% of all inputs), which have the effect of exciting the receiving neuron (making it more likely to get over threshold and fire an \"alarm\"). They are conveyed via a synaptic channel called **AMPA**, which is opened by the neurotransmitter **glutamate**.
-   **Inhibitory inputs** \-- these are the other 15% of inputs, which have the opposite effect to the excitatory inputs \-- they cause the neuron to be *less* likely to fire, and serve to make the integration process much more robust by keeping the excitation in check. There are specialized neurons in the brain called **inhibitory interneurons** that generate this inhibitory input (we\'ll learn a lot more about these in the [Networks](CCNBook/Networks#Inhibition "wikilink") chapter). This input comes in via **GABA** synaptic channels, driven by the neurotransmitter GABA.
-   **Leak inputs** \-- these aren\'t technically inputs, as they are always present and active, but they serve a similar function to the inhibitory inputs, by counteracting the excitation and keeping the neuron in balance overall. Biologically, leak channels are **potassium channels (K)**.

The inhibitory and excitatory inputs come from *different* neurons in the cortex: a given neuron can only send either excitatory or inhibitory outputs to other neurons, not both (although neurons in other brain areas do violate this constraint, neocortical pyramidal neurons appear to obey it). We will see the multiple implications of this constraint throughout the text.

Finally, we introduce the notion of the **net synaptic efficacy or <i>weight</i>**, which represents the total impact that a sending neuron activity signal can have on the receiving neuron, via its synaptic connection. *The synaptic weight is one of the most important concepts in the entire field of computational cognitive neuroscience!* We will be exploring it in many different ways as we go along. Biologically, it represents the net ability of the sending neuron\'s action potential to release **neurotransmitter**, and the ability of that neurotransmitter to open synaptic channels on the postsynaptic side (including the total number of such channels that are available to be opened). For the excitatory inputs, it is thus the amount of glutamate released by the sending neuron into the synapse, and the number and efficacy of AMPA channels on the receiving neuron\'s side of the synapse. Computationally, the weights determine what a neuron is detecting. A strong weight value indicates that the neuron is very sensitive to that particular input neuron, while a low weight means that that input is relatively unimportant. The entire process of [Learning](CCNBook/Learning "wikilink") amounts to changing these synaptic weights as a function of neural activity patterns in the sending and receiving neurons. In short, *everything you know, every cherished memory in your brain, is encoded as a pattern of synaptic weights!*

To learn more about the biology of the neuron, see [Neuron/Biology](CCNBook/Neuron/Biology "wikilink").

## Dynamics of Integration: Excitation vs. Inhibition and Leak

The process of integrating the three different types of input signals (excitation, inhibition, leak) lies at the heart of neural computation. This section provides a conceptual, intuitive understanding of this process, and how it relates to the underlying electrical properties of neurons. Later, we\'ll see how to translate this process into mathematical equations that can actually be simulated on the computer.

The integration process can be understood in terms of a **tug-of-war** (). This tug-of-war takes place in the space of **electrical potentials** that exist in the neuron relative to the surrounding extracellular medium in which neurons live (interestingly, this medium, and the insides of neurons and other cells as well, is basically salt water with sodium (Na+), chloride (Cl-) and other ions floating around \-- we carry our remote evolutionary environment around within us at all times). The core function of a neuron can be understood entirely in electrical terms: voltages (electrical potentials) and currents (flow of electrically charged ions in and out of the neuron through tiny pores called **ion channels**).

To see how this works, let\'s just consider excitation versus inhibition (inhibition and leak are effectively the same for our purposes at this time). The key point is that **the integration process reflects the relative strength of excitation versus inhibition** \-- if excitation is stronger than inhibition, then the neuron\'s electrical potential (voltage) increases, perhaps to the point of getting over threshold and firing an output action potential. If inhibition is stronger, then the neuron\'s electrical potential decreases, and thus moves further away from getting over the threshold for firing.

Before we consider specific cases, let\'s introduce some obscure terminology that neuroscientists use to label the various actors in our tug-of-war drama (going from left to right in the Figure):

-   <b>$g_i$</b> \-- the **inhibitory conductance** (*g* is the symbol for a conductance, and *i* indicates inhibition) \-- this is the total strength of the inhibitory input (i.e., how strong the inhibitory guy is tugging), and plays a major role in determining how strong of an inhibitory current there is. This corresponds biologically to the proportion of inhibitory ion channels that are currently open and allowing inhibitory ions to flow (these are **chloride** or **Cl-** ions in the case of GABA **inhibition**, and **potassium** or **K+** ions in the case of **leak** currents). For electricity buffs, the conductance is the inverse of resistance \-- most people find conductance more intuitive than resistance, so we\'ll stick with it.
-   <b>$E_i$</b> \-- the **inhibitory driving potential** \-- in the tug-of-war metaphor, this just amounts to where the inhibitory guy happens to be standing relative to the electrical potential scale that operates within the neuron. Typically, this value is around -75mV where **mV** stands for **millivolts** \-- one thousandth (1/1,000) of a volt. These are very small electrical potentials for very small neurons.
-   <b>$\Theta$</b> \-- the **action potential threshold** \-- this is the electrical potential at which the neuron will fire an action potential output to signal other neurons. This is typically around -50mV. This is also called the **firing threshold** or the **spiking threshold**, because neurons are described as \"firing a spike\" when they get over this threshold.
-   <b>$V_m$</b> \-- the **membrane potential** of the neuron (V = voltage or electrical potential, and m = membrane). This is the current electrical potential of the neuron relative to the extracellular space outside the neuron. It is called the membrane potential because it is the cell membrane (thin layer of fat basically) that separates the inside and outside of the neuron, and that is where the electrical potential really happens. An electrical potential or voltage is a relative comparison between the amount of electric charge in one location versus another. It is called a \"potential\" because when there is a difference, there is the potential to make stuff happen. For example, when there is a big potential difference between the charge in a cloud and that on the ground, it creates the potential for lightning. Just like water, differences in charge always flow \"downhill\" to try to balance things out. So if you have a lot of charge (water) in one location, it will flow until everything is all level. The cell membrane is effectively a dam against this flow, enabling the charge inside the cell to be different from that outside the cell. The ion channels in this context are like little tunnels in the dam wall that allow things to flow in a controlled manner. And when things flow, the membrane potential changes! In the tug-of-war metaphor, think of the membrane potential as the flag attached to the rope that marks where the balance of tugging is at the current moment.
-   <b>$E_e$</b> \-- the **excitatory driving potential** \-- this is where the excitatory guy is standing in the electrical potential space (typically around 0 mV).
-   <b>$g_e$</b> \-- the **excitatory conductance** \-- this is the total strength of the excitatory input, reflecting the proportion of excitatory ion channels that are open (these channels pass **sodium** or **Na+** ions \-- our deepest thoughts are all just salt water moving around).

shows specific cases in the tug-of-war scenario. In the first case, the excitatory conductance $g_e$ is very low (indicated by the small size of the excitatory guy), which represents a neuron at rest, not receiving many excitatory input signals from other neurons. In this case, the inhibition/leak pulls much more strongly, and keeps the membrane potential (Vm) down near the -70mV territory, which is also called the **resting potential** of the neuron. As such, it is below the action potential threshold $\Theta$, and so the neuron does not output any signals itself. Everyone is just chillin\'.

In the next case (b), the excitation is as strong as the inhibition, and this means that it can pull the membrane potential up to about the middle of the range. Because the firing threshold is toward the lower-end of the range, this is enough to get over threshold and fire a spike! The neuron will now communicate its signal to other neurons, and contribute to the overall flow of information in the brain\'s network.

The last case (c) is particularly interesting, because it illustrates that the integration process is fundamentally **relative** \-- what matters is how strong excitation is *relative* to the inhibition. If both are overall weaker, then neurons can still get over firing threshold. Can you think of any real-world example where this might be important? Consider the neurons in your visual system, which can experience huge variation in the overall amount of light coming into them depending on what you\'re looking at (e.g., compare snowboarding on a bright sunny day versus walking through thick woods after sunset). It turns out that the total amount of light coming into the visual system drives both a \"background\" level of inhibition, in addition to the amount of excitation that visual neurons experience. Thus, when it\'s bright, neurons get greater amounts of both excitation and inhibition compared to when it is dark. *This enables the neurons to remain in their sensitive range for detecting things* despite large differences in overall input levels.

## Computing Activation Output

The membrane potential Vm is not communicated directly to other neurons \-- instead it is subjected to a **threshold** and only the strongest levels of excitation are then communicated, resulting in a much more efficient and compact encoding of information in the brain. In human terms, neurons are sensitive to \"TMI\" (too much information) constraints, also known as \"Gricean Maxims\" [wikipedia link](http://en.wikipedia.org/wiki/Cooperative_principle) \-- e.g., only communicate relevant, important information.

Actual neurons in the Neocortex compute discrete **spikes** or **action potentials**, which are very brief (\< 1 ms) and trigger the release of neurotransmitter that then drives the excitation or inhibition of the neurons they are sending to. After the spike, the membrane potential Vm is reset back to a low value (at or even below the resting potential), and it must then climb back up again to the level of the threshold before another spike can occur. This process results in different *rates of spiking* associated with different levels of excitation \-- it is clear from eletrophysiological recordings of neurons all over the neocortex that this **spike rate** information is highly informative about behaviorally and cognitively relevant information. There remains considerable debate about the degree to which more precise differences in spike timing contain additional useful information.

In our computer models, we can simulate discrete spiking behavior directly in a very straightforward way (see below for details). However, we often use a **rate code** approximation instead, where the activation output of the neuron is a *real valued number* between 0-1 that corresponds to the overall rate of neural spiking. We typically think of this rate code as reflecting the net output of a small population of roughly 100 neurons that all respond to similar information \-- the neocortex is organized anatomically with **microcolumns** of roughly this number of neurons, where all of the neurons do indeed code for similar information. Use of this rate code activation enables smaller-scale models that converge on a stable interpretation of the input patterns rapidly, with an overall savings in computational time and model complexity. Nevertheless, there are tradeoffs in using these approximations, which we will discuss more in the [Networks](CCNBook/Networks "wikilink") and other chapters. Getting the rate code to produce a good approximation to discrete spiking behavior has been somewhat challenging in the Leabra framework, and only recently has a truly satisfactory solution been developed, which is now the standard in the [emergent](emergent "wikilink") software.

## Mathematical Formulations

Now you\'ve got an intuitive understanding of how the neuron integrates excitation and inhibition. We can capture this dynamic in a set of mathematical equations that can be used to simulate neurons on the computer. The first set of equations focuses on the effects of inputs to a neuron. The second set focuses on generating outputs from the neuron. We will cover a fair amount of mathematical ground here. Don\'t worry if you don\'t follow all of the details. As long as you follow conceptually what the equations are doing, you should be able to build on this understanding when you get your hands on the actual equations themselves and explore how they behave with different inputs and parameters. You will see that despite all the math, the neuron\'s behavior is indeed simple: the amount of excitatory input determines how excited it gets, in balance with the amount of inhibition and leak. And the resulting output signals behave pretty much as you would expect.

### Computing Inputs

We begin by formalizing the \"strength\" by which each side of the tug-of-war pulls, and then show how that causes the Vm \"flag\" to move as a result. This provides explicit equations for the tug-of-war dynamic integration process. Then, we show how to actually compute the conductance factors in this tug-of-war equation as a function of the inputs coming into the neuron, and the synaptic weights (focusing on the excitatory inputs for now). Finally, we provide a summary equation for the tug-of-war which can tell you where the flag will end up in the end, to complement the dynamical equations which show you how it moves over time.

#### Neural Integration

The key idea behind these equations is that each guy in the tug-of-war pulls with a strength that is proportional to both its overall strength (conductance), and how far the \"flag\" (Vm) is away from its position (indicated by the driving potential E). Imagine that the tuggers are planted in their position, and their arms are fully contracted when the Vm flag gets to their position (E), and they can\'t re-grip the rope, such that they can\'t pull any more at this point. To put this idea into an equation, we can write the \"force\" or **current** that the excitatory guy exerts as:

-   **excitatory current:**

:   $I_e = g_e \left(E_e-V_m\right)$

The excitatory current is $I_e$ (I is the traditional term for an electrical current, and e again for excitation), and it is the product of the conductance $g_e$ times *how far the membrane potential is away from the excitatory driving potential*. If $V_m = E_e$ then the excitatory guy has \"won\" the tug of war, and it no longer pulls anymore, and the current goes to zero (regardless of how big the conductance might be \-- anything times 0 is 0). Interestingly, this also means that the excitatory guy pulls the strongest when the Vm \"flag\" is furthest away from it \-- i.e., when the neuron is at its resting potential. Thus, it is easiest to excite a neuron when it\'s well rested.

The same basic equation can be written for the inhibition guy, and also separately for the leak guy (which we can now reintroduce as a basic clone of the inhibition term):

-   **inhibitory current:**

:   $I_i = g_i \left(E_i-V_m\right)$

-   **leak current:**

:   $I_l = g_l \left(E_l-V_m\right)$

(only the subscripts are different).

Next, we can add together these three different currents to get the **net current**, which represents the net flow of charged ions across the neuron\'s membrane (through the ion channels):

-   **net current:**

:   $I_{net} = I_e + I_i + I_l = g_e \left(E_e-V_m\right) + g_i \left(E_i-V_m\right) + g_l \left(E_l-V_m\right)$

So what good is a net current? Recall that electricity is like water, and it flows to even itself out. When water flows from a place where there is a lot of water to a place where there is less, the result is that there is less water in the first place and more in the second. The same thing happens with our currents: the flow of current changes the membrane potential (height of the water) inside the neuron:

-   **update of membrane potential due to net current:**

:   $V_m\left(t\right) = V_m\left(t-1\right) + dt_{vm} I_{net}$

($V_m(t)$ is the current value of Vm, which is updated from value on the previous time step $V_m(t-1)$, and the $dt_{vm}$ is a **rate constant** that determines how fast the membrane potential changes \-- it mainly reflects the capacitance of the neuron\'s membrane).

The above two equations are the essence of what we need to be able to simulate a neuron on a computer! It tells us how the membrane potential changes as a function of the inhibitory, leak and excitatory inputs \-- given specific numbers for these input conductances, and a starting Vm value, we can then **iteratively** compute the new Vm value according to the above equations, and this will accurately reflect how a real neuron would respond to similar such inputs!

To summarize, here\'s a single version of the above equations that does everything:

-   $V_m(t) = V_m(t-1) + dt_{vm} \left[ g_e (E_e-V_m) + g_i (E_i-V_m) + g_l (E_l-V_m) \right]$

For those of you who noticed the issue with the minus sign above, or are curious how all of this relates to **Ohm\'s law** and the process of diffusion, please see [Electrophysiology of the Neuron](CCNBook/Neuron/Electrophysiology "wikilink"). If you\'re happy enough with where we\'ve come, feel free to move along to finding out how we compute these input conductances, and what we then do with the Vm value to drive the output signal of the neuron.

#### Computing Input Conductances

The excitatory and inhibitory input conductances represent the total number of ion channels of each type that are currently open and thus allowing ions to flow. In real neurons, these conductances are typically measured in nanosiemens (nS), which is $10^{-9}$ siemens (a very small number \-- neurons are very tiny). Typically, neuroscientists divide these conductances into two components:

-   $\bar{g}$ (\"g-bar\") \-- a constant value that determines the **maximum conductance** that would occur if every ion channel were to be open.
-   $g\left(t\right)$ \-- a dynamically changing variable that indicates at the present moment, what fraction of the total number of ion channels are currently open (goes between 0 and 1).

Thus, the total conductances of interest are written as:

-   **excitatory conductance:**

:   $\bar{g_e} g_e(t)$

-   **inhibitory conductance:**

:   $\bar{g_i} g_i(t)$

-   **leak conductance:**

:   $\bar{g_l}$

(note that because leak is a constant, it does not have a dynamically changing value, only the constant g-bar value).

This separation of terms makes it easier to compute the conductance, because all we need to focus on is computing the proportion or fraction of open ion channels of each type. This can be done by computing the average number of ion channels open at each synaptic input to the neuron:

-   $g_e(t) = \frac{1}{n} \sum_i x_i w_i$

where $x_i$ is the **activity** of a particular sending neuron indexed by the subscript *i*, $w_i$ is the **synaptic weight strength** that connects sending neuron *i* to the receiving neuron, and *n* is the total number of channels of that type (in this case, excitatory) across all synaptic inputs to the cell. As noted above, the synaptic weight determines what patterns the receiving neuron is sensitive to, and is what adapts with learning \-- this equation shows how it enters mathematically into computing the total amount of excitatory conductance.

The above equation suggests that the neuron performs a very simple function to determine how much input it is getting: it just adds it all up from all of its different sources (and takes the average to compute a proportion instead of a sum \-- so that this proportion is then multiplied by g\_bar\_e to get an actual conductance value). Each input source contributes in proportion to how active the sender is, multiplied by how much the receiving neuron cares about that information \-- the synaptic weight value. We also refer to this average total input as the **net input**.

The same equation holds for inhibitory input conductances, which are computed in terms of the activations of inhibitory sending neurons, times the inhibitory weight values.

There are some further complexities about how we integrate inputs from different categories of input sources (i.e., projections from different source brain areas into a given receiving neuron), which we deal with in the optional subsection: [Net Input Detail](CCNBook/Neuron/NetInput "wikilink"). But overall, this aspect of the computation is relatively simple and we can now move on to the next step, of comparing the membrane potential to the threshold and generating some output.

#### Equilibrium Membrane Potential

Before finishing up the final step in the detection process (generating an output), we will need to use the concept of the **equilibrium membrane potential**, which is the value of Vm that the neuron will settle into and stay at, *given a fixed set of excitatory and inhibitory input conductances* (if these aren\'t steady, then the the Vm will likely be constantly changing as they change). This equilibrium value is interesting because it tells us more clearly how the tug-of-war process inside the neuron actually balances out in the end. Also, we will see in the next section that it is useful mathematically.

To compute the equilibrium membrane potential ($V_m^{eq}$), we can use an important mathematical technique: set the change in membrane potential (according to the iterative Vm updating equation from above) to 0, and then solve the equation for the value of Vm under this condition. In other words, if we want to find out what the equilibrium state is, we simply compute what the numbers need to be such that Vm is no longer changing (i.e., its rate of change is 0). Here are the mathematical steps that do this:

-   **iterative Vm update equation:**

:   $V_m(t) = V_m(t-1) + dt_{vm} \left[ g_e (E_e-V_m) + g_i (E_i-V_m) + g_l (E_l-V_m) \right]$

-   **just the change part (time constant omitted as we are looking for equilibrium):**

:   $\Delta V_m = g_e \left(E_e-V_m\right) + g_i (E_i-V_m) + g_l (E_l-V_m)$

-   **set it to zero:**

:   $0 = g_e \left(E_e-V_m\right) + g_i (E_i-V_m) + g_l (E_l-V_m)$

-   **solve for Vm:**

:   $V_m = \frac{g_e}{g_e + g_i + g_l} E_e + \frac{g_i}{g_e + g_i + g_l} E_i + \frac{g_l}{g_e + g_i + g_l} E_l$

We show the math here: [Equilibrium Membrane Potential Derivation](CCNBook/Neuron/Equilibrium_Membrane_Potential_Derivation "wikilink").

In words, this says that the excitatory drive $E_e$ contributes to the overall Vm as a function of the proportion of the excitatory conductance $g_e$ relative to the sum of all the conductances ($g_e + g_i + g_l$). And the same for each of the others (inhibition, leak). This is just what we expect from the tug-of-war picture: if we ignore g\_l, then the Vm \"flag\" is positioned as a function of the relative balance between $g_e$ and $g_i$ \-- if they are equal, then $\frac{g_e}{g_e + g_i}$ is .5 (e.g., just put a \"1\" in for each of the g\'s \-- 1/2 = .5), which means that the Vm flag is half-way between $E_i$ and $E_e$. So, all this math just to rediscover what we knew already intuitively! (Actually, that is the best way to do math \-- if you draw the right picture, it should tell you the answers before you do all the algebra). But we\'ll see that this math will come in handy next.

Here is a version with the conductance terms explicitly broken out into the \"g-bar\" constants and the time-varying \"g(t)\" parts:

-   $V_m = \frac{\bar{g_e}g_e(t)}{\bar{g_e}g_e(t) + \bar{g_i}g_i(t) + \bar{g_l}} E_e + \frac{\bar{g_i}g_i(t)}{\bar{g_e}g_e(t) + \bar{g_i}g_i(t) + \bar{g_l}} E_i + \frac{\bar{g_l}}{\bar{g_e}g_e(t) + \bar{g_i}g_i(t) + \bar{g_l}} E_l$

For those who really like math, the equilibrium membrane potential equation can be shown to be a [Bayesian Optimal Detector](CCNBook/Neuron/Bayesian_Detector "wikilink").

### Generating Outputs

The output of the neuron can be simulated at two different levels: discrete spiking (which is how neurons actually behave biologically), or using a rate code approximation. We cover each in turn, and show how the rate code must be derived to match the behavior of the discrete spiking neuron, when averaged over time (it is important that our approximations are valid in the sense that they match the more detailed biological behavior where possible, even as they provide some simplification).

#### Discrete Spiking

To compute discrete action potential spiking behavior from the neural equations we have so far, we need to determine when the membrane potential gets above the firing threshold, and then emit a spike, and subsequently reset the membrane potential back down to a value, from which it can then climb back up and trigger another spike again, etc. This is actually best expressed as a kind of simple computer program:

``` C
if (Vm > Theta) then: y = 1; Vm = Vm_r; else y = 0
```

where y is the activation output value of the neuron, and Vm\_r is the *reset potential* that the membrane potential is reset to after a spike is triggered. Biologically, there are special potassium (K+) channels that bring the membrane potential back down after a spike.

This simplest of spiking models is not *quite* sufficient to account for the detailed spiking behavior of actual cortical neurons. However, a slightly more complex model can account for actual spiking data with great accuracy (as shown by Gerstner and colleagues , and winning several international competitions even!). This model is known as the [Adaptive Exponential](CCNBook/Neuron/AdEx "wikilink") or AdEx model \-- click on the link to read more about it. We typically use this AdEx model when simulating discrete spiking, although the simpler model described above is also still an option. The critical feature of the AdEx model is that the effective firing threshold adapts over time, as a function of the excitation coming into the cell, and its recent firing history. The net result is a phenomenon called **spike rate adaptation**, where the rate of spiking tends to decrease over time for otherwise static input levels. Otherwise, however, the AdEx model is identical to the one described above.

#### Rate Code Approximation to Spiking

Even though actual neurons communicate via discrete spiking (action potential) events, it is often useful in our computational models to adopt a somewhat more abstract **rate code approximation**, where the neuron continuously outputs a single graded value (typically normalized between 0-1) that reflects the overall rate of spiking that the neuron should be exhibiting given the level of inputs it is receiving. In other words, we could count up the number of discrete spikes the neuron fires, and divide that by the amount of time we did the counting over, and this would give us an average spiking rate. Instead of having the neuron communicate this rate of spiking distributed in discrete spikes over that period of time, we can have it communicate that rate value instantly, as a graded number. Computationally, this should be more efficient, because it is compressing the amount of time required to communicate a particular spiking rate, and it also tends to reduce the overall level of noise in the network, because instead of switching between spiking and not-spiking, the neuron can continuously output a more steady rate code value.

As noted earlier, the rate code value can be thought of in biological terms as the output of a small population (e.g., 100) of neurons that are generally receiving the same inputs, and giving similar output responses \-- averaging the number of spikes at any given point in time over this population of neurons is roughly equivalent to averaging over time from a single spiking neuron. As such, we can consider our simulated rate code computational neurons to correspond to a small population of actual discrete spiking neurons.

To actually compute the rate code output, we need an equation that provides a real-valued number that matches the number of spikes emitted by a spiking neuron with the same level of inputs. Interestingly, you cannot use the membrane potential Vm as the input to this equation \-- it does *not* have a one-to-one relationship with spiking rate! That is, when we run our spiking model and measure the actual rate of spiking for different combinations of excitatory and inhibitory input, and then plot that against the equilibrium Vm value that those input values produce (without any spiking taking place), there are multiple spiking rate values for each Vm value \-- you cannot predict the correct firing rate value knowing only the Vm ().

Instead, it turns out that the excitatory net input $g_e$ enables a good prediction of actual spiking rate, when it is compared to an appropriate threshold value (). For the membrane potential, we know that Vm is compared to the threshold $\Theta$ to determine when output occurs. What is the appropriate threshold to use for the excitatory net input? We need to somehow convert $\Theta$ into a $g_e^{\Theta}$ value \-- a threshold in excitatory input terms. Here, we can leverage the equilibrium membrane potential equation, derived above. We can use this equation to solve for the level of excitatory input conductance that would put the equilibrium membrane potential right at the firing threshold $\Theta$:

-   **equilibrium Vm at threshold:**

:   $\Theta = \frac{g_e^{\Theta} E_e + g_i E_i + g_l E_l}{g_e^{\Theta} + g_i + g_l}$

-   **solved for g\_e\_theta:**

:   $g_e^{\Theta} = \frac{g_i (E_i - \Theta) + g_l (E_l  - \Theta)}{\Theta - E_e}$

(see [g\_e\_theta derivation](CCNBook/Neuron/g_e_theta_derivation "wikilink") for the algebra to derive this solution),

Now, we can say that our rate coded output activation value will be some function of the difference between the excitatory net input g\_e and this threshold value:

-   $y = f(g_e - g_e^{\Theta})$

And all we need to do is figure out what this function f() should look like.

There are three important properties that this function should have:

-   **threshold** \-- it should be 0 (or close to it) when g\_e is less than its threshold value (neurons should not respond when below threshold).
-   **saturation** \-- when g\_e gets very strong relative to the threshold, the neuron cannot actually keep firing at increasingly high rates \-- there is an upper limit to how fast it can spike (typically around 100-200 Hz or spikes per second). Thus, our rate code function also needs to exhibit this leveling-off or saturation at the high end.
-   **smoothness** \-- there shouldn\'t be any abrupt transitions (sharp edges) to the function, so that the neuron\'s behavior is smooth and continuous.

0\) and the Noisy-XX1 (NXX1) function (Noise {{=}} .005).}}

The **X-over-X-plus-1 (XX1)** function (, Noise=0 case, also known as the [Michaelis-Mentin kinetics function](http://en.wikipedia.org/wiki/Michaelis–Menten_kinetics) \-- wikipedia link) exhibits the first two of these properties:

-   $f_{xx1}(x) = \frac{x}{x+1}$

where *x* is the *positive* portion of $g_e - g_e^{\Theta}$, with an extra **gain** factor $\gamma$, which just multiplies everything:

-   $x = \gamma [g_e - g_e^{\Theta}]_+$

So the full equation is:

-   $y = \frac{\gamma [g_e - g_e^{\Theta}]_+}{\gamma [g_e - g_e^{\Theta}]_+ + 1}$

Which can also be written as:

-   $y = \frac{1}{\left(1 + \frac{1}{\gamma [g_e - g_e^{\Theta}]_+} \right)}$

As you can see in (Noise=0), the basic XX1 function is not smooth at the point of the threshold. To remedy this problem, we **convolve** the XX1 function with normally-distributed (gaussian) noise, which smooths it out as shown in the Noise=0.005 case in . Convolving amounts to adding to each point in the function some contribution from its nearby neighbors, weighted by the gaussian (bell-shaped) curve. It is what photo editing programs do when they do \"smoothing\" or \"blurring\" on an image. In the software, we perform this convolution operation and then store the results in a lookup table of values, to make the computation very fast. Biologically, this convolution process reflects the fact that neurons experience a large amount of noise (random fluctuations in the inputs and membrane potential), so that even if they are slightly below the firing threshold, a random fluctuation can sometimes push it over threshold and generate a spike. Thus, the spiking rate around the threshold is smooth, not sharp as in the plain XX1 function.

For completeness sake, and strictly for the mathematically inclined, here is the equation for the convolution operation:

-   $y^*(x) = \int_{-\infty}^{\infty} \frac{1}{\sqrt{2 \pi} \sigma} e^{-z^2/(2 \sigma^2)} y(z-x) dz$

where y(z-x) is the XX1 function applied to the z-x input instead of just x. In practice, a finite kernel of width $3 \sigma$ on either side of x is used in the numerical convolution.

After convolution, the XX1 function () approximates the average firing rate of many neuronal models with discrete spiking, including AdEx. A mathematical explanation is here: [Frequency-Current Curve](CCNBook/Neuron/Frequency_Current_Curve "wikilink").

#### Restoring Iterative Dynamics in the Activation

There is just one last problem with the equations as written above. They don\'t evolve over time in a graded fashion. In contrast, the Vm value does evolve in a graded fashion by virtue of being iteratively computed, where it incrementally approaches the equilibrium value over a number of time steps of updating. Instead the activation produced by the above equations goes directly to its equilibrium value very quickly, because it is calculated based on excitatory conductance and does not take into account the sluggishness with which changes in conductance lead to changes in membrane potentials (due to capacitance). As discussed in the [Introduction](CCNBook/Intro "wikilink"), graded processing is very important, and we can see this very directly in this case, because the above equations do not work very well in many cases because they lack this gradual evolution over time.

To introduce graded iterative dynamics into the activation function, we just use the activation value ($y^*(x)$) from the above equation as a *driving force* to an iterative temporally-extended update equation:

:   $y(t) = y(t-1) + dt_{vm} \left(y^*(x) - y(t-1) \right)$

This causes the actual final rate code activation output at the current time *t*, y(t) to iteratively approach the driving value given by $y^*(x)$, with the same time constant $dt_{vm}$ that is used in updating the membrane potential. In practice this works extremely well, better than any prior activation function used with Leabra.

### Summary of Neuron Equations and Normalized Parameters


**Table 2.1:** The parameters used in our simulations are normalized using the above conversion factors so that the typical values that arise in a simulation fall within the 0..1 normalized range. For example, the membrane potential is represented in the range between 0 and 2 where 0 corresponds to -100mV and 2 corresponds to +100mV and 1 is thus 0mV (and most membrane potential values stay within 0-1 in this scale). The biological values given are the default values for the AdEx model. Other biological values can be input using the BioParams button on the LeabraUnitSpec, which automatically converts them to normalized values.

Table 2.1 shows the normalized values of the parameters used in our simulations. We use these normalized values instead of the normal biological parameters so that everything fits naturally within a 0..1 range, thereby simplifying many practical aspects of working with the simulations.

The final equations used to update the neuron, in computational order, are shown here, with all variables that change over time indicated as a function of (t):

1\. Compute the excitatory input conductance (inhibition would be similar, but we\'ll discuss this more in the next chapter, so we\'ll omit it here):

-   $g_e(t) = \frac{1}{n} \sum_i x_i(t) w_i$

2\. Update the membrane potential one time step at a time, as a function of input conductances (separating conductances into dynamic and constant \"g-bar\" parts):

-   $V_m(t) = V_m(t-1) + dt_{vm} \left[ \bar{g}_e g_e(t) (E_e-V_m) + \bar{g}_i g_i(t) (E_i-V_m) + g_l (E_l-V_m) \right]$

3a. For discrete spiking, compare membrane potential to threshold and trigger a spike and reset Vm if above threshold:

``` C
if (Vm(t) > Theta) then: y(t) = 1; Vm(t) = Vm_r; else y(t) = 0`
```

3b. For rate code approximation, compute output activation as NXX1 function of g\_e and Vm:

-   $y^*(x) = f_{NXX1}(g_e^*(t)) \approx \frac{1}{\left(1 + \frac{1}{\gamma [g_e - g_e^{\Theta}]_+} \right)}$ (convolution with noise not shown)
-   $y(t) = y(t-1) + dt_{vm} \left(y^*(x) - y(t-1) \right)$ (restoring iterative dynamics based on time constant of membrane potential changes)

## Exploration of the Individual Neuron

To get your hands dirty, run [Neuron](CCNBook/Sims/Neuron/Neuron "wikilink"). As this is the first exploration you\'ll be running, you may need to consult the overall page for information on installing the Emergent software etc: [CCNBook/Sims/All](CCNBook/Sims/All "wikilink").

## Back to the Detector

Now that you can see how the individual neuron integrates a given excitatory signal relative to leak/inhibition, it is important to put this into the larger perspective of the detection process. In this simulation, you\'ll see how a neuron can pick out a particular input pattern from a set of inputs, and also how it can have different patterns of responding depending on its parameters (\"loose\" or \"strict\").

To run this exploration, go to [Detector](CCNBook/Sims/Neuron/Detector "wikilink").

## SubTopics

Here are all the sub-topics within the Neuron chapter, collected in one place for easy browsing. These may or may not be optional for a given course, depending on the instructor\'s specifications of what to read:

-   [Neuron Biology](CCNBook/Neuron/Biology "wikilink") \-- more detailed description of neuron biology.
-   [Neuron Electrophysiology](CCNBook/Neuron/Electrophysiology "wikilink") \-- more detailed description of the electrophysiology of the neuron, and how the underlying concentration gradients of ions give rise to the electrical integration properties of the neuron.
-   [Net Input Detail](CCNBook/Neuron/NetInput "wikilink") \-- details on how net inputs are computed across multiple different input projections.
-   [Adaptive Exponential Spiking Model](CCNBook/Neuron/AdEx "wikilink") \-- the AdEx model has won multiple competitions for best fitting actual cortical neuron firing patterns, and is what we actually use in spiking mode output.
-   [Temporal Dynamics](CCNBook/Neuron/Temporal_Dynamics "wikilink") \-- longer time-scale temporal dynamics of neurons (adaptation and hysteresis currents, and synaptic depression).
-   [Sigmoidal Unit Activation Function](CCNBook/Neuron/SigmoidUnits "wikilink") \-- a more abstract formalism for simulating the behavior of neurons, used in more abstract neural network models (e.g., backpropagation models).
-   [Bayesian Optimal Detector](CCNBook/Neuron/Bayesian_Detector "wikilink") \-- how the equilibrium membrane potential represents a Bayesian optimal way of integrating the different inputs to the neuron.

## Explorations

Here are all the explorations covered in the main portion of the Neuron chapter:

-   [Neuron](CCNBook/Sims/Neuron/Neuron "wikilink") (neuron.proj) \-- Individual Neuron \-- spiking and rate code activation. (**Questions 2.1 - 2.7**)
-   [Detector](CCNBook/Sims/Neuron/Detector "wikilink") (detector.proj) \-- The neuron as a detector \-- demonstrates the critical function of synaptic weights in determining what a neuron detects. (**Questions 2.8 - 2.10**)

## External Resources
