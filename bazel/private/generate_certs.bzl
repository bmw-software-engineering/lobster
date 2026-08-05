"""Bazel rule to generate self-signed SSL certificates for testing.

This rule generates self-signed X.509 certificates using OpenSSL, suitable for
HTTPS testing scenarios (e.g., codebeamer mock server).

The generated files (cert.pem, key.pem) are deterministic and cacheable, and
can be referenced as build outputs or included in filegroups.
"""

def _generate_certs_impl(ctx):
    """Generate self-signed SSL certificate and private key.

    Args:
        ctx: Bazel rule context.

    Returns:
        DefaultInfo with generated cert.pem and key.pem files.
    """
    cert = ctx.actions.declare_file("cert.pem")
    key = ctx.actions.declare_file("key.pem")

    # Use run_shell to invoke openssl from system PATH
    # This avoids needing an external openssl Bazel dependency
    ctx.actions.run_shell(
        command = """
            openssl req -x509 -newkey rsa:2048 -nodes \
                -keyout "{key}" \
                -out "{cert}" \
                -days 365 \
                -subj "/CN=localhost"
        """.format(
            key = key.path,
            cert = cert.path,
        ),
        outputs = [cert, key],
        progress_message = "Generating SSL certificates (cert.pem, key.pem)",
    )

    return [
        DefaultInfo(files = depset([cert, key])),
    ]

generate_certs = rule(
    implementation = _generate_certs_impl,
    doc = """Generate self-signed SSL certificates for testing.
    
    Produces two files: cert.pem (certificate) and key.pem (private key).
    Uses system openssl command.
    
    Example:
        generate_certs(name = "certs")
        
        filegroup(
            name = "test_data",
            srcs = [":certs"],
        )
    """,
)
