import logging
from typing import Set

from golem.managers import ProposalManagerPlugin
from golem.resources import Proposal
from golem.utils.logging import trace_span

logger = logging.getLogger(__name__)


class BlacklistProviderIdPlugin(ProposalManagerPlugin):
    def __init__(self, blacklist: Set[str]) -> None:
        self._blacklist = blacklist

    @trace_span(show_results=True)
    async def get_proposal(self) -> Proposal:
        while True:
            proposal: Proposal = await self._get_proposal()
            proposal_data = await proposal.get_data()
            provider_id = proposal_data.issuer_id

            if provider_id not in self._blacklist:
                return proposal

            if not proposal.initial:
                await proposal.reject("provider_id is on blacklist")

            logger.debug(
                "Provider `%s` from proposal `%s` is on blacklist, picking different proposal...",
                provider_id,
                proposal,
            )
