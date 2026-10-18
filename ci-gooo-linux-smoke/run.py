# Copyright (c) 2026, Compiler Explorer Authors
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#     * Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
"""Draft: fixed-input Linux CLI and real app.ts HTTP smoke, not generated Go execution."""
import argparse
import gzip
import hashlib
import json
import os
from pathlib import Path
import platform
import resource
import select
import shutil
import signal
import socket
import struct
import subprocess
import tarfile
import time
import urllib.error
import urllib.parse
import urllib.request

SOURCE = '1dc2708e90f99566308a5dd587efad02c62fa45d'
PRODUCER = '83928fa4538245abe33b08549da47f8cbdc50ed2'
ASSET_URL = 'https://github.com/kimjooyoon/meta-ontology-go/releases/download/v0.6.32-dev/gooo-linux-amd64.tar.gz'
ARCHIVE_SHA = 'e7d9735d72f23d5d9dd2eaac48c2cd81431c8f6e59b41d9282d307996eb87253'
BINARY_SHA = '9b5e42857237caac6204cba0c8a349dc5cb7228a1e59117110cb979dc8c5dabe'
MIB = 1024 * 1024
EVIDENCE_CAP = 2 * MIB
CONTRACT = {'schema': 'ce9258-linux-smoke-source-contract/v1',
 'source_commit': '1dc2708e90f99566308a5dd587efad02c62fa45d',
 'source_tree': '5083d4a2ec1aef686ddb3ba8ecb1d430031a818b',
 'base_commit': '5f2e213e69d45a4a20757cefd5309c0373c2fe28',
 'source_path_count': 21,
 'paths': [{'path': '.github/labeler.yml',
            'bytes': 14703,
            'sha256': '4b099bcc4d0770780b2aec79f3c728046cbf4f82dc595713db838557ae71c59b'},
           {'path': 'docs/Gooo.md',
            'bytes': 2705,
            'sha256': '6722612cf679815999baa6a5486d212866a0ca84f72ce32f2957ba64fb9c5d26'},
           {'path': 'etc/config/gooo.amazon.properties',
            'bytes': 915,
            'sha256': 'cdeadf9f5ef5a9adb50ec75372f90bb7d5af96a6d41a405b24e6b57270b42e95'},
           {'path': 'etc/config/gooo.defaults.properties',
            'bytes': 846,
            'sha256': 'd412eb59dce1586ea937f787ae5716e6f01a53f6503c6850e3366ef964936a1d'},
           {'path': 'examples/gooo/default.gooo',
            'bytes': 176,
            'sha256': 'e12057f83aa3cc880563a13f2aee801c28f50c3abefbbf183a969b96ebbe8e3d'},
           {'path': 'lib/compilers/_all.ts',
            'bytes': 9040,
            'sha256': 'b0ec50f5f336d9ca4cedc9fb1a4e202964aa0a5a2f382625c62f45c76a3aec0e'},
           {'path': 'lib/compilers/gooo.ts',
            'bytes': 11416,
            'sha256': '91cb1f102c2d6510c5e1937c14ec45042188e34d5d95f3efe895eefa1349bb64'},
           {'path': 'lib/languages.ts',
            'bytes': 34602,
            'sha256': 'd06950bf2c07da884ccca4437046b7c4952353d264448c40ce5fc24c1195cf2b'},
           {'path': 'public/logos/gooo.svg',
            'bytes': 268,
            'sha256': '50710c30dd4c55c55ac14bbb197b24de1e1df8b11421cf7a7e85e767f6b29d9f'},
           {'path': 'static/modes/_all.ts',
            'bytes': 2970,
            'sha256': '181652f4a6bf058e604c84d86e92814d3878cd51d0018b7eeafb3748f5f3dc86'},
           {'path': 'static/modes/gooo-mode.ts',
            'bytes': 2467,
            'sha256': 'f454fea95bf069672fd82eb1b566bee7d4540c8d1195d0b1d839026ceafcc206'},
           {'path': 'test/fixtures/gooo/build-identity-darwin.json',
            'bytes': 648,
            'sha256': '9e61c23a1302e7390ba03af0606066a8cca1b13d5bd96864dc3c27a85c00dd5c'},
           {'path': 'test/fixtures/gooo/changed.gooo',
            'bytes': 172,
            'sha256': '64fe09258df8b2cfd661610bc549a3073926e395e2b8a929fc857e5554e16162'},
           {'path': 'test/fixtures/gooo/changed.json',
            'bytes': 14555,
            'sha256': '7f49e15285092f7145b99f80a551e05fc4aad3ea57a4ee9dff02c6c8c3a82f46'},
           {'path': 'test/fixtures/gooo/fail-closed.json',
            'bytes': 14100,
            'sha256': '016978b4bc801303917a17f8328a8883be1f891fec006db2e3ac9ef8bcaa38c8'},
           {'path': 'test/fixtures/gooo/provenance.json',
            'bytes': 1720,
            'sha256': '6932f9b7f040da29f329dd04c0b3b23d6e413b85e8a5155be77724fb358ca967'},
           {'path': 'test/fixtures/gooo/repeat.json',
            'bytes': 14559,
            'sha256': '75e751119aefdca8b3f542c99f9e26c3b21d68d58b8c252bcdeaeacf438efe9c'},
           {'path': 'test/fixtures/gooo/valid.gooo',
            'bytes': 176,
            'sha256': 'e12057f83aa3cc880563a13f2aee801c28f50c3abefbbf183a969b96ebbe8e3d'},
           {'path': 'test/fixtures/gooo/valid.json',
            'bytes': 14559,
            'sha256': '75e751119aefdca8b3f542c99f9e26c3b21d68d58b8c252bcdeaeacf438efe9c'},
           {'path': 'test/gooo-tests.ts',
            'bytes': 16826,
            'sha256': '6cff58ce527c174cc774ce1e2566c42b2808783948fe363ca63cbfd71884a707'},
           {'path': 'types/languages.interfaces.ts',
            'bytes': 4733,
            'sha256': '96dd2b8a05a18101895332971b696c1cc554c666cb07f0bd83f6049138c31601'}],
 'test_only_delta_allowlist': ['.github/workflows/gooo-linux-smoke.yml', 'ci-gooo-linux-smoke/run.py']}
ALLOWED_DOWNLOAD_HOSTS = {'github.com', 'release-assets.githubusercontent.com', 'objects.githubusercontent.com'}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def save(name, value):
    (EVIDENCE / name).write_text(json.dumps(value, indent=2) + '\n')


def source_check():
    if ARGS.phase == 'runtime':
        require(RUNTIME_IDENTITY_READY and os.getuid() == os.geteuid() == ARGS.uid,
                'No runtime source Git read before the runner identity is established')
    def git(*argv):
        p = subprocess.run(['git', *argv], cwd=REPO, stdin=subprocess.DEVNULL,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=5, check=True)
        require(len(p.stdout) + len(p.stderr) < 65536, 'Git metadata output cap')
        return p.stdout.decode().strip()
    contract = CONTRACT
    require(contract['source_commit'] == SOURCE and contract['source_path_count'] == 21, 'Source contract identity')
    require(git('rev-parse', 'HEAD^') == SOURCE, 'Test branch must have one normal commit directly above 1dc')
    changed = set(git('diff', '--name-only', SOURCE, 'HEAD').splitlines())
    require(changed == set(contract['test_only_delta_allowlist']), 'Only the two test-only additions are allowed')
    require(not git('diff', '--name-only', 'HEAD'), 'Tracked source differs from the test-branch commit')
    for item in contract['paths']:
        raw = (REPO / item['path']).read_bytes()
        require(len(raw) == item['bytes'] and sha(raw) == item['sha256'], 'Pinned feature source mismatch: ' + item['path'])
    return {'source_commit': SOURCE, 'source_tree': contract['source_tree'], 'test_branch_head': git('rev-parse', 'HEAD'),
            'feature_paths': 21, 'contract_sha256': sha(json.dumps(CONTRACT, sort_keys=True).encode()),
            'all_other_tracked_source_equal_to_1dc': True}


def controlled_env():
    return {'PATH': str(NODE.parent) + ':/usr/bin:/bin', 'HOME': str(WORK / 'home'),
            'TMPDIR': str(WORK / 'tmp'), 'NODE_ENV': 'production', 'NODE_OPTIONS': '--max-old-space-size=1536',
            'GOOO_LAYA_URL': '', 'GOOO_LAYA_API_KEY': '', 'AWS_EC2_METADATA_DISABLED': 'true',
            'CYPRESS_INSTALL_BINARY': '0', 'npm_config_cache': str(WORK / 'npm-cache'),
            'npm_config_update_notifier': 'false', 'LANG': 'C.UTF-8'}


def limits():
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    resource.setrlimit(resource.RLIMIT_FSIZE, (256 * MIB, 256 * MIB))
    resource.setrlimit(resource.RLIMIT_CPU, (300, 300))
    resource.setrlimit(resource.RLIMIT_NOFILE, (1024, 1024))
    cpus = sorted(os.sched_getaffinity(0))
    os.sched_setaffinity(0, cpus[:2])


class Owned:
    def __init__(self, label, argv, seconds, log_cap=256 * 1024):
        self.label, self.argv, self.cap = label, argv, log_cap
        self.paths = [EVIDENCE / (label + '.stdout'), EVIDENCE / (label + '.stderr')]
        self.files = [p.open('xb') for p in self.paths]
        self.started = time.monotonic()
        self.deadline = self.started + seconds
        self.max_rss = 0
        self.closed = False
        self.captured = 0
        self.eof = set()
        try:
            self.p = subprocess.Popen(argv, cwd=REPO, env=controlled_env(), stdin=subprocess.DEVNULL,
                                      stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True,
                                      preexec_fn=limits)
        except BaseException:
            for file in self.files:
                file.close()
            raise
        # Register immediately; even a journal failure must close this exact child.
        OWNED.append(self)
        self.pipes = [self.p.stdout, self.p.stderr]
        for pipe in self.pipes:
            os.set_blocking(pipe.fileno(), False)
        save(label + '-started.json', {'pid': self.p.pid, 'pgid': self.p.pid, 'argv': argv})

    def pump(self):
        active = [pipe for i, pipe in enumerate(self.pipes) if i not in self.eof]
        for pipe in select.select(active, [], [], 0)[0]:
            index = self.pipes.index(pipe)
            while True:
                remaining = self.cap - self.captured
                require(remaining > 0, self.label + ': output capture cap reached; EOF unproven')
                try:
                    chunk = os.read(pipe.fileno(), min(65536, remaining))
                except BlockingIOError:
                    break
                if not chunk:
                    self.eof.add(index)
                    break
                self.captured += len(chunk)
                self.files[index].write(chunk)
                self.files[index].flush()

    def check(self):
        self.pump()
        require(time.monotonic() < self.deadline, self.label + ': wall-clock cap')
        require(sum(p.stat().st_size for p in self.paths) <= self.cap, self.label + ': output cap')
        rss = 0
        for path in Path('/proc').glob('[0-9]*/stat'):
            try:
                # /proc stat comm may contain spaces; fields after its last ')' start with state.
                fields = path.read_text().rsplit(')', 1)[1].split()
                if int(fields[2]) == self.p.pid:
                    rss += int(fields[21]) * os.sysconf('SC_PAGE_SIZE')
            except (FileNotFoundError, ProcessLookupError):
                pass
        self.max_rss = max(self.max_rss, rss)
        require(rss <= 2 * 1024 * MIB, self.label + ': process-group RSS cap')

    def wait(self):
        while self.p.poll() is None:
            self.check()
            time.sleep(0.05)
        self.check()
        code = self.p.wait(timeout=2)
        self.close()
        return code, self.paths[0].read_bytes(), self.paths[1].read_bytes()

    def close(self):
        if self.closed:
            return
        # Clean the exact owned group even if its leader already exited.
        for sig in (signal.SIGTERM, signal.SIGKILL):
            try:
                os.killpg(self.p.pid, sig)
            except ProcessLookupError:
                break
            end = time.monotonic() + 3
            while time.monotonic() < end:
                self.p.poll()
                try:
                    os.killpg(self.p.pid, 0)
                except ProcessLookupError:
                    break
                time.sleep(0.05)
            else:
                continue
            break
        code = self.p.wait(timeout=3)
        try:
            os.killpg(self.p.pid, 0)
            absent = False
        except ProcessLookupError:
            absent = True
        capture_error = None
        try:
            self.pump()
        except BaseException as error:
            capture_error = type(error).__name__
        for pipe in self.pipes:
            pipe.close()
        for file in self.files:
            file.close()
        self.closed = True
        save(self.label + '-process.json', {'pid': self.p.pid, 'exit': code, 'wait_completed': True,
             'process_group_absent': absent, 'seconds': time.monotonic() - self.started,
             'observed_peak_group_rss_bytes': self.max_rss, 'stream_capture_complete': len(self.eof) == 2,
             'captured_output_bytes': self.captured, 'capture_error': capture_error,
             'streams': [{'name': p.name, 'bytes': p.stat().st_size, 'sha256': sha(p.read_bytes())} for p in self.paths]})
        require(absent, self.label + ': owned process group remains')
        require(capture_error is None and len(self.eof) == 2, self.label + ': incomplete original stream capture')


def run(label, argv, seconds=15, log_cap=256 * 1024):
    return Owned(label, argv, seconds, log_cap).wait()


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def download():
    # Each redirect response is read and counted; signed locations stay in memory only.
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect())
    url, received, records = ASSET_URL, 0, []
    deadline = time.monotonic() + 60
    for hop in range(5):
        parsed = urllib.parse.urlsplit(url)
        require(parsed.scheme == 'https' and parsed.hostname in ALLOWED_DOWNLOAD_HOSTS and not parsed.username,
                'Unexpected release redirect host or scheme')
        require(time.monotonic() < deadline, 'Release download deadline')
        request = urllib.request.Request(url, headers={'Accept-Encoding': 'identity', 'User-Agent': 'CE9258-linux-smoke'})
        try:
            response = opener.open(request, timeout=min(15, deadline - time.monotonic()))
        except urllib.error.HTTPError as error:
            response = error
        with response:
            status = response.status
            cap = 16 * MIB - received if status == 200 else min(65536, 16 * MIB - received)
            data, digest, count, eof = bytearray(), hashlib.sha256(), 0, False
            try:
                while True:
                    require(time.monotonic() < deadline, 'Release body deadline')
                    require(count < cap, 'Release response cap reached; EOF unproven')
                    chunk = response.read(min(65536, cap - count))
                    if not chunk:
                        eof = True
                        break
                    count += len(chunk)
                    received += len(chunk)
                    digest.update(chunk)
                    if status == 200:
                        data.extend(chunk)
            finally:
                records.append({'hop': hop, 'host': parsed.hostname, 'status': status, 'bytes_returned': count,
                                'sha256_of_returned_bytes': digest.hexdigest(), 'EOF_reached': eof})
                save('release-http.json', {'responses': records, 'observed_returned_body_bytes': received,
                     'returned_body_cap_bytes': 16 * MIB, 'strict_actual_total_proven': all(r['EOF_reached'] for r in records),
                     'unknown_body_reservation_bytes': 0 if eof else 65536,
                     'scope': 'HTTP response body bytes returned by this reader; excludes headers/TLS/wire overhead'})
            if status in (301, 302, 303, 307, 308):
                require(response.headers.get('Location') is not None, 'Missing release redirect')
                url = urllib.parse.urljoin(url, response.headers['Location'])
                continue
            require(status == 200, 'Release download non-success status')
            require(len(data) == 13993818 and sha(data) == ARCHIVE_SHA, 'Release archive size or digest mismatch')
            (WORK / 'gooo-linux-amd64.tar.gz').write_bytes(data)
            return
    raise RuntimeError('Release redirect limit')


def unpack():
    archive, expanded = WORK / 'gooo-linux-amd64.tar.gz', WORK / 'expanded.tar'
    total = 0
    with gzip.open(archive, 'rb') as src, expanded.open('xb') as dst:
        while True:
            chunk = src.read(65536)
            if not chunk:
                break
            total += len(chunk)
            require(total <= 32 * MIB, 'Expanded archive cap')
            dst.write(chunk)
    with tarfile.open(expanded, 'r:') as tar:
        members = tar.getmembers()
        require(len(members) == 1, 'Release must contain exactly one member')
        item = members[0]
        require(item.name == 'gooo' and item.isfile() and item.size == 26136648 and item.mode == 0o755,
                'Unexpected release layout/type/mode')
        raw = tar.extractfile(item).read(item.size + 1)
        require(len(raw) == item.size and sha(raw) == BINARY_SHA, 'Extracted compiler digest mismatch')
    require(raw[:6] == b'\x7fELF\x02\x01' and struct.unpack_from('<H', raw, 18)[0] == 62, 'Not Linux ELF64 amd64')
    offset = struct.unpack_from('<Q', raw, 32)[0]
    size, count = struct.unpack_from('<HH', raw, 54)
    require(size >= 56 and count < 1024 and offset + size * count <= len(raw), 'ELF program-header bounds')
    kinds = [struct.unpack_from('<I', raw, offset + size * i)[0] for i in range(count)]
    require(2 not in kinds and 3 not in kinds, 'Unexpected dynamic loader/dependency')
    binary = WORK / 'gooo'
    binary.write_bytes(raw)
    binary.chmod(0o755)
    save('release-integrity.json', {'archive_bytes': archive.stat().st_size, 'archive_sha256': ARCHIVE_SHA,
         'binary_bytes': len(raw), 'binary_sha256': BINARY_SHA, 'ELF_machine': 62,
         'PT_INTERP_present': False, 'PT_DYNAMIC_present': False, 'safe_single_regular_entry': True})
    expanded.unlink()


def identity(value):
    expected = {'schema': 'gooo/build-identity/v1', 'version': '0.6.32-dev', 'compiler_source_sha': PRODUCER,
                'vcs_revision': PRODUCER, 'build_info_observed': True, 'go_version': 'go1.27.2',
                'native_go_required': 'go1.27.2', 'source_status': 'CLEAN_VCS', 'vcs_modified': 'false'}
    for key, wanted in expected.items():
        require(type(value.get(key)) is type(wanted) and value[key] == wanted, 'Build identity mismatch: ' + key)


def generated(raw, input_bytes):
    value = json.loads(raw)
    require(isinstance(value, dict) and set(value) == {'report', 'source'}, 'Success envelope mismatch')
    report, source = value['report'], value['source']
    require(isinstance(source, str) and source.strip(), 'Empty generated source')
    for key, wanted in {'schema': 'gooo/body-codegen-report/v3', 'decision': 'PASS', 'activity': 'Double',
                        'compiler_source_sha': PRODUCER, 'typecheck_passed': True,
                        'deterministic_replay': True, 'repository_writes': 0}.items():
        require(type(report.get(key)) is type(wanted) and report[key] == wanted, 'Body report mismatch: ' + key)
    require('error' not in report, 'Success report has an error')
    require(report['source_digest'] == 'sha256:' + sha(input_bytes), 'Input digest mismatch')
    require(report['generated_digest'] == report['replay_digest'] == 'sha256:' + sha(source.encode()), 'Emission/replay digest mismatch')
    require(report['completeness_receipt']['profile_id'] == 'gooo/body-codegen-pure-v1' and
            report['completeness_receipt']['scope']['compiler_source_sha'] == PRODUCER, 'Completeness scope mismatch')
    for key in ('plan_sha256', 'program_digest'):
        text = report[key]
        require(isinstance(text, str) and text.startswith('sha256:') and len(text) == 71 and
                all(c in '0123456789abcdef' for c in text[7:]), 'Malformed report digest')
    return source


def enter_runtime_namespace():
    global RUNTIME_IDENTITY_READY
    # Complete namespace setup and privilege dropping before any source Git read.
    require(os.geteuid() == 0 and ARGS.uid > 0 and ARGS.gid > 0, 'Isolated namespace/drop-privilege precondition')
    require(REPO.stat().st_uid == ARGS.uid and WORK.stat().st_uid == ARGS.uid,
            'Runner must own workspace and smoke work directory')
    require(os.getpid() == 1, 'Runtime must be PID1 of its own PID namespace')
    require(os.readlink('/proc/self/ns/pid') != ARGS.host_pidns and
            os.readlink('/proc/1/ns/pid') == os.readlink('/proc/self/ns/pid'),
            'PID namespace or private /proc view was not established')
    require(os.readlink('/proc/self/ns/mnt') != ARGS.host_mntns, 'Private mount namespace was not established')
    require(os.readlink('/proc/self/ns/net') != ARGS.host_netns, 'Network namespace was not isolated')
    result = subprocess.run(['/usr/sbin/ip', 'link', 'set', 'lo', 'up'], stdin=subprocess.DEVNULL,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=3)
    require(result.returncode == 0 and len(result.stdout) + len(result.stderr) < 4096, 'Loopback setup failed')
    interfaces = {line.split(':', 1)[0].strip() for line in Path('/proc/net/dev').read_text().splitlines()[2:]}
    require(interfaces == {'lo'}, 'Isolated namespace has external interfaces')
    os.setgroups([])
    os.setgid(ARGS.gid)
    os.setuid(ARGS.uid)
    require(os.getuid() == os.geteuid() == ARGS.uid and os.getgid() == os.getegid() == ARGS.gid
            and os.getgroups() == [], 'Privilege drop failed')
    RUNTIME_IDENTITY_READY = True
    save('runtime-isolation.json', {'network_namespace_distinct': True, 'interfaces': ['lo'],
         'uid': os.geteuid(), 'PID1': True, 'private_proc_view': True,
         'PID_namespace': os.readlink('/proc/self/ns/pid'), 'mount_namespace_distinct': True,
         'model_URL_and_key_blank': True, 'generated_Go_execution': False,
         'CE_sandboxType': 'none (unchanged defaults)', 'production_nsjail_validation': False})



def launch_namespace():
    # Only namespace supervision runs privileged; no source Git/compiler calls here.
    require(os.geteuid() == 0 and ARGS.uid > 0 and ARGS.gid > 0, 'Privileged launcher precondition')
    os.umask(0o022)
    argv = ['/usr/bin/unshare', '--mount', '--pid', '--fork', '--mount-proc=/proc', '--net',
            '--propagation', 'private', '--kill-child=SIGTERM', '--', '/usr/bin/python3',
            str(Path(__file__).resolve()), 'runtime', '--source', str(REPO), '--work', str(WORK),
            '--node', str(NODE), '--uid', str(ARGS.uid), '--gid', str(ARGS.gid),
            '--host-netns', os.readlink('/proc/self/ns/net'),
            '--host-pidns', os.readlink('/proc/self/ns/pid'),
            '--host-mntns', os.readlink('/proc/self/ns/mnt')]
    code, _, _ = run('namespace-init', argv, 210)
    inner = EVIDENCE / 'runtime-receipt.json'
    isolation = EVIDENCE / 'runtime-isolation.json'
    known_init = inner.exists() and isolation.exists() and json.loads(isolation.read_bytes()).get('PID1') is True
    save('namespace-containment.json', {'unshare_wait_exit': code,
         'runtime_init_receipt_present': known_init,
         'namespace_init_exit_observed_via_unshare_fork_wait': known_init,
         'kernel_PID_namespace_teardown_containment': known_init,
         'per_detached_child_waits_all_observed': False,
         'scope': 'unshare --fork waits for namespace PID1; PID1 exit triggers kernel termination of remaining namespace processes; not an observed wait for each child'})
    require(code == 0 and known_init and json.loads(inner.read_bytes())['status'] == 'RUNTIME_CHECKS_PASS_CONTAINMENT_PENDING',
            'Isolated runtime failed; preserve original inner evidence')


def cleanup_pid_namespace():
    require(os.getpid() == 1 and RUNTIME_IDENTITY_READY and
            os.readlink('/proc/self/ns/pid') != ARGS.host_pidns, 'Namespace cleanup identity guard')
    reaped, signals = [], []

    def snapshot():
        rows = []
        for path in Path('/proc').glob('[0-9]*/stat'):
            if path.parent.name == '1':
                continue
            try:
                fields = path.read_text().rsplit(')', 1)[1].split()
                rows.append({'pid': int(path.parent.name), 'state': fields[0], 'ppid': int(fields[1]),
                             'pgid': int(fields[2]), 'uid': path.parent.stat().st_uid})
            except (FileNotFoundError, ProcessLookupError):
                pass
            require(len(rows) <= 256, 'Namespace cleanup snapshot cap')
        return rows

    def reap():
        for _ in range(512):
            try:
                pid, status = os.waitpid(-1, os.WNOHANG)
            except ChildProcessError:
                return
            if pid == 0:
                return
            reaped.append({'pid': pid, 'wait_status': status, 'exit': os.waitstatus_to_exitcode(status)})
        raise RuntimeError('Namespace adopted-child reap cap')

    before = snapshot()
    remaining = before
    for sig in (signal.SIGTERM, signal.SIGKILL):
        for row in remaining:
            try:
                os.kill(row['pid'], sig)
                signals.append({'pid': row['pid'], 'signal': int(sig), 'sent': True})
            except ProcessLookupError:
                pass
            except PermissionError:
                signals.append({'pid': row['pid'], 'signal': int(sig), 'sent': False})
        deadline = time.monotonic() + 2
        while time.monotonic() < deadline:
            reap()
            remaining = snapshot()
            if not remaining:
                break
            time.sleep(0.05)
        if not remaining:
            break
    save('namespace-child-cleanup.json', {'visible_snapshot_before': before, 'signals': signals,
         'actually_reaped_adopted_children': reaped, 'last_visible_snapshot': remaining,
         'last_visible_snapshot_empty': not remaining, 'scope': 'private PID namespace /proc only; finite snapshots, not an all-OS census',
         'unobserved_detached_children_may_exist_between_snapshots': True,
         'final_containment_requires_outer_observed_PID1_exit': True,
         'per_detached_child_waits_all_observed': False})


def freeze_artifact(phase_receipt):
    approved = WORK / 'approved-artifact'
    stage = WORK / 'approved-artifact.staging'
    require(not approved.exists() and not stage.exists(), 'Do not rerun artifact collection in the same work directory')

    def validate():
        rows = []
        for path in sorted(EVIDENCE.iterdir()):
            require(path.is_file() and not path.is_symlink() and path.suffix in ('.json', '.stdout', '.stderr'),
                    'Artifact allowlist violation')
            require(path.stat().st_size <= MIB, 'Artifact member cap')
            raw = path.read_bytes()
            rows.append({'name': path.name, 'bytes': len(raw), 'sha256': sha(raw)})
        require(sum(row['bytes'] for row in rows) < EVIDENCE_CAP - 65536, 'Artifact total cap')
        return rows

    rejection = None
    try:
        validate()
    except BaseException as error:
        rejection = type(error).__name__
    if rejection:
        phase_receipt['status'] = 'FAIL'
        phase_receipt['artifact_gate_rejected'] = True
        phase_receipt['artifact_gate_error_type'] = rejection
    save('artifact-receipt.json', phase_receipt)
    stage.mkdir()
    if rejection:
        # Rejected raw content stays local; only this small synthetic receipt is approved.
        (stage / 'artifact-gate.json').write_text(json.dumps({'status': 'REJECTED',
            'original_evidence_preserved_locally': True, 'rejected_content_uploaded': False,
            'error_type': rejection, 'producer_phase_success_required_for_valid_evidence': False}, indent=2) + '\n')
    else:
        rows = validate()
        for row in rows:
            raw = (EVIDENCE / row['name']).read_bytes()
            require(len(raw) == row['bytes'] and sha(raw) == row['sha256'], 'Evidence changed during freeze')
            (stage / row['name']).write_bytes(raw)
        (stage / 'artifact-manifest.json').write_text(json.dumps({'files': rows,
            'binaries_archives_dependencies_and_source_excluded': True}, indent=2) + '\n')
    require(sum(path.stat().st_size for path in stage.iterdir()) <= EVIDENCE_CAP, 'Approved artifact cap')
    stage.rename(approved)
    # Set readiness even for valid producer FAIL evidence; never point at raw evidence/.
    output = os.environ.get('GITHUB_OUTPUT')
    require(output is not None and '\n' not in str(approved), 'Workflow artifact output path missing')
    with open(output, 'a') as handle:
        handle.write('artifact_ready=true\nartifact_path=' + str(approved) + '\n')
    return rejection


def runtime():
    require(RUNTIME_IDENTITY_READY and os.geteuid() == ARGS.uid, 'Runtime identity was not established')
    require(sha((WORK / 'gooo').read_bytes()) == BINARY_SHA, 'Compiler changed after prepare')
    binary, fixtures = str(WORK / 'gooo'), REPO / 'test/fixtures/gooo'
    code, stdout, _ = run('cli-version', [binary, 'version', '--build', '--json'])
    require(code == 0, 'Actual Linux version command failed')
    identity(json.loads(stdout))
    outputs, repeated = [], []
    for label, filename, fixture in [('valid', 'valid.gooo', 'valid.json'), ('repeat', 'valid.gooo', 'repeat.json'),
                                     ('changed', 'changed.gooo', 'changed.json')]:
        data = (fixtures / filename).read_bytes()
        target = WORK / filename
        target.write_bytes(data)
        code, stdout, _ = run('cli-' + label, [binary, 'body-codegen', '--json', '--activity', 'Double', str(target)])
        require(code == 0, 'Actual Linux body-codegen failed: ' + label)
        source = generated(stdout, data)
        require(source == json.loads((fixtures / fixture).read_bytes())['source'], 'Linux emission differs from saved source')
        outputs.append(source)
        repeated.append(stdout)
    require(repeated[0] == repeated[1] and outputs[0] == outputs[1] != outputs[2], 'Repeat/change relation failed')
    invalid = (fixtures / 'valid.gooo').read_text().replace('input + input', 'input0 + input0')
    require(invalid != (fixtures / 'valid.gooo').read_text(), 'Invalid input construction failed')
    (WORK / 'invalid.gooo').write_text(invalid)
    code, stdout, _ = run('cli-fail-closed', [binary, 'body-codegen', '--json', '--activity', 'Double', str(WORK / 'invalid.gooo')])
    failure = json.loads(stdout)
    require(code == 1 and failure['schema'] == 'gooo/body-codegen-report/v3' and failure['decision'] == 'FAIL_CLOSED'
            and failure['source'] == '' and failure['compiler_source_sha'] == PRODUCER
            and type(failure['repository_writes']) is int and failure['repository_writes'] == 0
            and 'report' not in failure and 'undefined: input0' in failure['error'], 'Flat refusal contract failed')
    save('cli-verdict.json', {'actual_Linux_amd64_execution': True, 'producer': PRODUCER, 'build_identity_checked': True,
         'valid_repeat_stdout_byte_exact': True, 'changed_emission_differs': True, 'flat_failure_exit': code,
         'source_sha256': [sha(s.encode()) for s in outputs], 'generated_Go_execution': False})
    config = WORK / 'etc/config'
    config.mkdir(parents=True)
    defaults = list((REPO / 'etc/config').glob('*.defaults.properties'))
    require(sum(p.stat().st_size for p in defaults) < 4 * MIB, 'Config-copy cap')
    for path in defaults:
        shutil.copyfile(path, config / path.name)
    shutil.copyfile(REPO / 'etc/config/sponsors.yaml', config / 'sponsors.yaml')
    (config / 'gooo.smoke.properties').write_text('compiler.gooo_body_83928fa.exe=' + binary + '\n')
    (config / 'compiler-explorer.smoke.properties').write_text(
        'cacheConfig=\nexecutableCacheConfig=\ncompilerCacheConfig=\nstorageSolution=null\ncompileTimeoutMs=7500\n'
        'maxConcurrentCompiles=1\nmaxUploadSize=1mb\nthirdPartyIntegrationEnabled=false\nstatusTrackingEnabled=false\n'
        'remoteExecutionArchitectures=\ntempDirCleanupSecs=3600\n')
    (config / 'aws.smoke.properties').write_text('region=\n')
    with socket.socket() as probe:
        probe.bind(('127.0.0.1', 0))
        port = probe.getsockname()[1]
    base = 'http://127.0.0.1:' + str(port)
    server = Owned('server', [str(NODE), '--import=tsx', 'app.ts', '--env', 'smoke', '--root-dir', str(WORK / 'etc'),
                   '--host', '127.0.0.1', '--port', str(port), '--language', 'gooo', '--no-cache', '--no-local',
                   '--no-remote-fetch', '--exit-on-compiler-failure', '--tmp-dir', str(WORK / 'tmp')], 90)
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect())
    start = time.monotonic()
    while True:
        server.check()
        require(server.p.poll() is None and time.monotonic() - start < 30, 'CE startup failed or exceeded 30s')
        try:
            with opener.open(base + '/api/compilers/gooo', timeout=0.5) as response:
                require(response.status == 200 and len(response.read(65537)) <= 65536, 'Readiness HTTP bound')
                break
        except (urllib.error.URLError, TimeoutError):
            time.sleep(0.1)
    requests = []

    def request(label, route, payload=None):
        server.check()
        raw = None if payload is None else json.dumps(payload).encode()
        req = urllib.request.Request(base + route, data=raw,
              headers={'Accept': 'application/json', 'Content-Type': 'application/json'})
        with opener.open(req, timeout=12) as response:
            raw = response.read(65537)
            require(len(raw) <= 65536, 'CE HTTP body cap')
            (EVIDENCE / (label + '.json')).write_bytes(raw)
            requests.append({'label': label, 'route': route, 'status': response.status, 'bytes': len(raw), 'sha256': sha(raw)})
            save('http-ledger.json', requests)
            require(response.status == 200, 'CE HTTP status')
            server.check()
            return json.loads(raw)

    def body(source, options='--activity Double', execute=False):
        return {'source': source, 'lang': 'gooo', 'options': {'userArguments': options,
                'filters': {'execute': execute, 'binary': False}, 'compilerOptions': {'skipAsm': False}}}

    def no_execution(result):
        require(not result.get('didExecute') and 'execResult' not in result, 'Unexpected execution result')

    def source_result(result, expected):
        require(result['code'] == 0 and not result.get('timedOut') and result['languageId'] == 'go', 'CE source result failed')
        no_execution(result)
        require(all(set(line) == {'text'} for line in result['asm']), 'Fabricated assembly metadata')
        require('\n'.join(line['text'] for line in result['asm']) == expected, 'CE source differs from CLI source')

    compilers = request('01-compilers', '/api/compilers/gooo?fields=all')
    require(len(compilers) == 1 and compilers[0]['id'] == 'gooo_body_83928fa', 'Compiler discovery mismatch')
    for key in ('supportsExecute', 'supportsBinary', 'supportsBinaryObject'):
        require(compilers[0][key] is False, 'Unsupported capability advertised: ' + key)
    identity(json.loads(compilers[0]['fullVersion']))
    route = '/api/compiler/gooo_body_83928fa/compile'
    valid, changed = (fixtures / 'valid.gooo').read_text(), (fixtures / 'changed.gooo').read_text()
    for label, source, expected in [('02-valid', valid, outputs[0]), ('03-repeat', valid, outputs[1]), ('04-changed', changed, outputs[2])]:
        source_result(request(label, route, body(source)), expected)
    executor = body(valid)
    executor['options']['compilerOptions']['executorRequest'] = True
    for label, payload in [('05-fail-closed', body(invalid)), ('06-invalid-options', body(valid, '--output /tmp/untrusted.go')),
                           ('07-execution-refused', executor)]:
        result = request(label, route, payload)
        require(result['code'] != 0 and result.get('asm', []) in ([], [{'text': '<Compilation failed>'}]), 'Refusal contains partial source')
        no_execution(result)
        if label == '07-execution-refused':
            require(result.get('didExecute') is False, 'Explicit executor did not refuse')
    source_result(request('08-unsupported-execute-filter', route, body(valid, execute=True)), outputs[0])
    server.close()
    save('http-verdict.json', {'status': 'PASS', 'real_app_ts_HTTP_cases': len(requests), 'bind': '127.0.0.1',
         'explicit_executor_refused': True, 'unsupported_execute_filter_ignored_without_execution': True,
         'no_partial_source_on_failures': True, 'generated_Go_execution': False})


def main():
    require(platform.system() == 'Linux' and platform.machine() == 'x86_64', 'Linux amd64 required')
    require(NODE.is_file() and REPO.is_dir(), 'Node/source prerequisites missing')
    # No implicit download/install/runtime recovery; the first failure ends this attempt.
    if ARGS.phase == 'launch':
        launch_namespace()
        return
    if ARGS.phase == 'runtime':
        enter_runtime_namespace()
    pins = source_check()
    save(ARGS.phase + '-source-before.json', pins)
    if ARGS.phase == 'prepare':
        require(os.environ.get('GITHUB_REPOSITORY') == 'kimjooyoon/compiler-explorer' and
                os.environ.get('GITHUB_REF') == 'refs/heads/test/gooo-linux-smoke-839-r2', 'Fork/branch guard')
        require(not (REPO / 'node_modules').exists(), 'Use a fresh checkout; do not repair a previous attempt')
        code, stdout, _ = run('node-version', [str(NODE), '--version'])
        require(code == 0 and stdout.strip() == b'v22.23.1', 'Pinned Node version mismatch')
        npm = NODE.parent / 'npm'
        code, _, _ = run('dependencies', [str(npm), 'exec', '--yes', '--package=npm@11.2.0', '--', 'npm',
                        'ci', '--include=dev', '--no-audit', '--no-fund'], 300, MIB)
        require(code == 0, 'Pinned npm ci failed')
        require(sum(p.stat().st_size for p in (REPO / 'node_modules').rglob('*') if p.is_file() and not p.is_symlink())
                < 3 * 1024 * MIB, 'Dependency logical-size cap')
        download()
        unpack()
    elif ARGS.phase == 'runtime':
        runtime()
    else:
        return
    save(ARGS.phase + '-source-after.json', source_check())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('phase', choices=['prepare', 'launch', 'runtime', 'artifact'])
    parser.add_argument('--source', required=True)
    parser.add_argument('--work', required=True)
    parser.add_argument('--node', required=True)
    parser.add_argument('--uid', type=int, default=-1)
    parser.add_argument('--gid', type=int, default=-1)
    parser.add_argument('--host-netns', default='')
    parser.add_argument('--host-pidns', default='')
    parser.add_argument('--host-mntns', default='')
    ARGS = parser.parse_args()
    REPO, WORK, NODE = Path(ARGS.source).resolve(), Path(ARGS.work).resolve(), Path(ARGS.node).resolve()
    require(WORK.is_absolute() and WORK != REPO and REPO not in WORK.parents, 'Work must be outside source')
    for directory in (WORK, WORK / 'evidence', WORK / 'home', WORK / 'tmp'):
        directory.mkdir(parents=True, exist_ok=True)
    EVIDENCE, OWNED = WORK / 'evidence', []
    RUNTIME_IDENTITY_READY = False
    def interrupted(signum, _frame):
        raise InterruptedError('Smoke interrupted by signal ' + str(signum))
    signal.signal(signal.SIGINT, interrupted)
    signal.signal(signal.SIGTERM, interrupted)
    started, failure = time.monotonic(), None
    try:
        main()
    except BaseException as error:
        # Exceptions can contain signed redirect URLs; only phase/class are retained here.
        failure = {'phase': ARGS.phase, 'exception_type': type(error).__name__,
                   'message': str(error) if isinstance(error, RuntimeError) else 'See bounded original command streams; URL-bearing exception text withheld'}
    finally:
        cleanup_errors = []
        for child in reversed(OWNED):
            try:
                child.close()
            except BaseException as error:
                cleanup_errors.append(type(error).__name__)
        if ARGS.phase == 'runtime' and RUNTIME_IDENTITY_READY:
            try:
                cleanup_pid_namespace()
            except BaseException as error:
                cleanup_errors.append('namespace-cleanup:' + type(error).__name__)
        try:
            if ARGS.phase not in ('runtime', 'launch') or (ARGS.phase == 'runtime' and RUNTIME_IDENTITY_READY):
                save(ARGS.phase + '-source-final.json', source_check())
            else:
                save(ARGS.phase + '-source-final.json', {'status': 'NOT_READ',
                     'reason': 'Privileged outer launch or incomplete runner identity: source Git read not permitted'})
        except BaseException as error:
            if failure is None:
                failure = {'phase': 'final source check', 'exception_type': type(error).__name__}
        if ARGS.phase == 'artifact':
            phases = {}
            for phase in ('prepare', 'runtime', 'launch'):
                path = EVIDENCE / (phase + '-receipt.json')
                phases[phase] = json.loads(path.read_bytes()) if path.exists() else {'status': 'NOT_RUN'}
            containment_path = EVIDENCE / 'namespace-containment.json'
            containment = json.loads(containment_path.read_bytes()) if containment_path.exists() else {}
            complete = (phases['prepare']['status'] == phases['launch']['status'] == 'PASS' and
                        phases['runtime']['status'] == 'RUNTIME_CHECKS_PASS_CONTAINMENT_PENDING' and
                        containment.get('kernel_PID_namespace_teardown_containment') is True)
            if failure is None and not complete:
                failure = {'phase': 'artifact aggregation', 'prior_phase_statuses': phases,
                           'outer_namespace_teardown_confirmed': containment.get('kernel_PID_namespace_teardown_containment') is True}
        phase_status = 'FAIL' if failure or cleanup_errors else ('RUNTIME_CHECKS_PASS_CONTAINMENT_PENDING' if ARGS.phase == 'runtime' else 'PASS')
        phase_receipt = {'status': phase_status,
             'first_failure': failure, 'cleanup_errors': cleanup_errors, 'duration_seconds': time.monotonic() - started,
             'direct_Popen_groups': len(OWNED), 'all_direct_Popen_handles_closed': all(child.closed for child in OWNED),
             'detached_descendant_waits_all_observed': False,
             'containment_pending_outer_init_wait': ARGS.phase == 'runtime',
             'generated_Go_execution': False, 'production_sandbox_validation': False}
        if ARGS.phase == 'artifact':
            rejection = freeze_artifact(phase_receipt)
            if rejection and failure is None:
                failure = {'phase': 'artifact gate', 'error_type': rejection}
        else:
            save(ARGS.phase + '-receipt.json', phase_receipt)
    raise SystemExit(1 if failure or cleanup_errors else 0)
