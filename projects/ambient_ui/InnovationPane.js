
class InnovationPane {
  constructor(glintStream) {
    this.glintStream = glintStream;
    this.container = this.createContainer();
    this.glintStream.addEventListener('innovation.proposal', (event) => {
      this.renderProposals(event.detail.proposals);
    });
  }

  createContainer() {
    const container = document.createElement('div');
    container.id = 'innovation-pane';
    container.style.position = 'fixed';
    container.style.bottom = '20px';
    container.style.left = '20px';
    container.style.width = '400px';
    container.style.backgroundColor = 'rgba(0, 0, 0, 0.8)';
    container.style.color = 'white';
    container.style.padding = '15px';
    container.style.borderRadius = '10px';
    container.style.fontFamily = 'monospace';
    container.style.maxHeight = '40%';
    container.style.overflowY = 'auto';
    document.body.appendChild(container);
    return container;
  }

  renderProposals(proposals) {
    for (const proposal of proposals) {
      const proposalElement = this.createProposalElement(proposal);
      this.container.prepend(proposalElement);
    }
  }

  createProposalElement(proposal) {
    const element = document.createElement('div');
    element.className = 'proposal-card';
    element.style.marginBottom = '10px';
    element.style.paddingBottom = '10px';
    element.style.borderBottom = '1px solid #555';

    const title = document.createElement('h4');
    title.textContent = `Proposal: ${proposal.type}`;
    element.appendChild(title);

    const rationale = document.createElement('p');
    rationale.textContent = proposal.rationale;
    element.appendChild(rationale);

    const inspectButton = document.createElement('button');
    inspectButton.textContent = 'Inspect';
    inspectButton.onclick = () => {
      // This would likely open a modal with the full JSON
      console.log(JSON.stringify(proposal.draft, null, 2));
      alert('Check the console for the full proposal draft.');
    };
    element.appendChild(inspectButton);

    const acceptButton = document.createElement('button');
    acceptButton.textContent = 'Accept';
    acceptButton.onclick = () => {
      // This would trigger the innovatecraft CLI or a direct API call
      console.log(`Accepting proposal ${proposal.id}...`);
      element.remove();
    };
    element.appendChild(acceptButton);

    const rejectButton = document.createElement('button');
    rejectButton.textContent = 'Reject';
    rejectButton.onclick = () => {
      // This would trigger the innovatecraft CLI or a direct API call
      console.log(`Rejecting proposal ${proposal.id}...`);
      element.remove();
    };
    element.appendChild(rejectButton);

    return element;
  }
}

// Example usage:
// const glintStream = new EventTarget();
// const innovationPane = new InnovationPane(glintStream);
//
// glintStream.dispatchEvent(new CustomEvent('innovation.proposal', {
//   detail: {
//     proposals: [{
//       id: 'prop-123',
//       type: 'new_glyph',
//       draft: { id: 'glyph.new.test', description: 'A test glyph.' },
//       rationale: 'A test proposal.'
//     }]
//   }
// }));
