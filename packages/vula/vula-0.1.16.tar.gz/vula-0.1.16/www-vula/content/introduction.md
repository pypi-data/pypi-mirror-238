---
title: "Introduction"
date: 2021-08-04T18:45:53+02:00
draft: false
---
With zero configuration, Vula automatically encrypts IP communication between
hosts on a local area network in a forward-secret and transitionally
post-quantum manner to protect against passive eavesdropping.

With manual key verification and/or automatic key pinning and manual resolution
of IP or hostname conflicts, Vula will additionally protect against
interception by active adversaries.

When the local gateway to the internet is also Vula peer, internet-destined
traffic will also be encrypted on the LAN.

### How does it work?

Automatically.

Vula combines [WireGuard](https://www.wireguard.com/papers/wireguard.pdf) for
forward-secret point-to-point tunnels with
[mDNS](https://tools.ietf.org/html/rfc6762) and
[DNS-SD](https://tools.ietf.org/html/rfc6763) for local service announcements,
and enhances the confidentiality of WireGuard tunnels by using
[CSIDH](https://csidh.isogeny.org/), a post-quantum non-interactive key
exchange primitive, to generate a peer-wise pre-shared key for each tunnel
configuration.

Vula's advantages over some other solutions include:

* design is absent of single points of failure (SPOFs)
* uses existing IP addresses inside and outside of the tunnels, allowing
  seamless integration into existing LAN environments using DHCP and/or manual
  addressing
* avoids needing to attempt handshakes with non-participating hosts
* does not require any configuration to disrupt passive surveillance
  adversaries
* simple verification with QR codes to disrupt active surveillance adversaries

See [`NOTES`](/notes/) for
some discussion of the threat model and other technical details, and
[`COMPARISON`](/comparison/)
for a comparison of Vula to some related projects.

### Current status

Vula is functional today, although it has some known issues documented in
[`STATUS`](/status/). It is
ready for daily use by people who are proficient with Linux networking and the
command line, but we do not yet recommend it for people who are not.

See [`INSTALL`](/install/) for
installation and usage instructions.

See [`HACKING`](/hacking/) for
some tips on opening the hood.

### Security contact

We consider this project to currently be alpha pre-release, experimental,
research quality code.  It is not yet suitable for widespread deployment.  It
has not yet been audited by an independent third party and it should be treated
with caution.

If you or someone you know finds a security issue - please [open an
issue](https://codeberg.org/vula/vula/issues/new) or feel free to send an email
to `security at vula dot link`.

Our current bug bounty for security issues is humble. We will credit the
reporter for their finding, and when possible, we will treat qualifying
reporters to a beverage after the COVID-19 crisis has ended; ojalá. Locations
limited to qualifying CCC events such as the yearly Congress.

### Authors

The authors of vula are anonymous for now, while our paper is undergoing peer
review.

### Acknowledgements

[`OPERATION_VULA`](/operation-vula/)
has some history about the name Vula.

Vula is not associated with or endorsed by the
[WireGuard](https://www.wireguard.com/) project. WireGuard is a registered
trademark of [Jason A.  Donenfeld](https://www.zx2c4.com/).
